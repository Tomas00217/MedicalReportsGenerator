import logging
import copy
from string import Template
from typing import Any, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.language import Language, MedicalReportBlock
from data.data_objects import DiagnosisData, OnsetData, AdmissionData, TreatmentData, \
    PostAcuteCareData, PostStrokeComplicationsData, EtiologyData, DischargeData, MedicationData, \
    DiagnosisOcclusionsData, ImagingTreatmentData, RiskFactorsData, PriorTreatmentData, PatientData, ImagingData
from data.models import Diagnosis, Onset, Admission, Thrombolysis, Thrombectomy, Treatment, \
    PostAcuteCare, PostStrokeComplications, Etiology, Discharge, MedicalReport, Patient, FollowUpImaging
from pathlib import Path


class TemplateWithPeriods(Template):
    """
    Class representing a Template with custom pattern.
    The pattern accepts periods in the values which should be replaced.

    """
    idpattern = r'(?-i:[._a-zA-Z][._a-zA-Z0-9]*)'


class MedicalReportsGenerator:
    """
    A class representing the medical report generator.

    Serves to generate the medical report piece by piece.

    Methods
    -------
    generate_medical_report(data)
        Loads the jinja2 template and renders the template with generated structure
    """

    def __init__(self, language: Language, template_filepath: Path):
        """

        Parameters
        ----------
        language : Language
            Loaded language variant of the dictionary
        template_filepath : Path
            File path towards the template
        """

        self.language = language
        self.filepath = template_filepath
        self.data = {}
        self.transported = False

    def generate_medical_report(self, data: Any) -> str:
        """Loads the jinja2 template and renders the template with generated structure

        Parameters
        ----------
        data : Any
            Data of the patient from the database

        Returns
        -------
        str
            Generated medical report with all the values substituted
        """

        path = self.filepath.parent
        file = self.filepath.name

        env = Environment(loader=FileSystemLoader(path), autoescape=select_autoescape())
        template = env.get_template(file)

        self.data = data
        report = self.__generate_structure()

        return template.render(report=report)

    def __generate_structure(self) -> dict:
        """Generates the whole structure of a medical report with replaced string template values

        Returns
        -------
        dict
            Medical report as a dict to be used for jinja2 template
        """

        medical_report = self.__create_medical_report()

        # We create a deep copy of dictionary with variables from medical report for the purpose of condition evaluation
        # while parsing, these variables are then translated and used for substitution
        variables = copy.deepcopy(medical_report.to_dict())
        translations = self.__translate_variables(medical_report)
        scoped_values = self.__prepare_scoped_values(translations)

        report = {
            "diagnosis": self.__get_substituted_block(self.language.diagnosis, medical_report.diagnosis,
                                                      variables, scoped_values),

            "patient": self.__get_substituted_block(self.language.patient, medical_report.patient,
                                                    variables, scoped_values),

            "onset": self.__get_substituted_block(self.language.onset, medical_report.onset,
                                                  variables, scoped_values),


            "admission": self.__get_substituted_block(self.language.admission, medical_report.admission,
                                                      variables, scoped_values),


            "treatment": self.__get_substituted_block(self.language.treatment, medical_report.treatment,
                                                      variables, scoped_values),


            "follow_up_imaging": self.__get_substituted_block(self.language.follow_up_imaging,
                                                              medical_report.follow_up_imaging, variables, scoped_values),


            "post_acute_care": self.__get_substituted_block(self.language.post_acute_care, medical_report.post_acute_care,
                                                            variables, scoped_values),

            "post_stroke_complications": self.__get_substituted_block(self.language.post_stroke_complications,
                                                                      medical_report.post_stroke_complications,
                                                                      variables, scoped_values),


            "etiology": self.__get_substituted_block(self.language.etiology, medical_report.etiology,
                                                     variables, scoped_values),


            "discharge": self.__get_substituted_block(self.language.discharge, medical_report.discharge,
                                                      variables, scoped_values),

        }

        return report

    @staticmethod
    def __get_substituted_block(language_block: MedicalReportBlock, generated_block: Any,
                                variables: dict, scoped_values: dict) -> str:
        """Gets the block result and substitutes it with values


        Parameters
        ----------
        language_block : MedicalReportBlock
            A block from the language class defining the structure
        generated_block : Any
            Generated block by the generator
        variables : dict
            Variables used to get the block result
        scoped_values : dict
            Values used for substitution

        Returns
        -------
        str
            block result with substitutions

        """
        return TemplateWithPeriods(language_block.get_block_result(variables) if generated_block else "")\
            .safe_substitute(scoped_values)

    def __create_medical_report(self) -> MedicalReport:
        """Creates the whole MedicalReport from all of its parts

        Returns
        -------
        MedicalReport
            The whole medical report with all the template values yet to be replaced
        """

        return MedicalReport(self.__create_diagnosis(),
                             self.__create_patient(),
                             self.__create_onset(),
                             self.__create_admission(),
                             self.__create_treatment(),
                             self.__create_follow_up_imaging(),
                             self.__create_post_acute_care(),
                             self.__create_post_stroke_complications(),
                             self.__create_etiology(),
                             self.__create_discharge())

    def __create_diagnosis(self) -> Diagnosis:
        """Creates the Diagnosis part of MedicalReport

        Returns
        -------
        Diagnosis
            The diagnosis part medical report with all the template values yet to be replaced
        """

        diagnosis_data = DiagnosisData.from_dict(self.data)
        diagnosis_occlusions = DiagnosisOcclusionsData.from_dict(self.data)

        diagnosis = Diagnosis(diagnosis_data.stroke_type,
                              diagnosis_data.aspects_score,
                              diagnosis_data.imaging_type,
                              self.__parse_data(self.__get_variables("occlusion_position"), vars(diagnosis_occlusions)),
                              diagnosis_data.imaging_timestamp,
                              diagnosis_data.imaging_within_hour,
                              self.__get_setting("time_format"))

        return diagnosis

    def __create_patient(self) -> Patient:
        """Creates the Patient part of MedicalReport

        Returns
        -------
        Patient
            The patient part medical report with all the template values yet to be replaced
        """

        patient_data = PatientData.from_dict(self.data)
        risk_factors_data = RiskFactorsData.from_dict(self.data)
        prior_treatment_data = PriorTreatmentData.from_dict(self.data)
        risk_atrial_fib = {"risk_atrial_fibrilation": patient_data.risk_atrial_fibrilation}

        patient = Patient(patient_data.patient_id,
                          patient_data.age,
                          patient_data.sex,
                          self.__parse_data(self.__get_variables("risk_factors"), vars(risk_factors_data)),
                          self.__parse_data(self.__get_variables("prior_treatment"), vars(prior_treatment_data)),
                          self.__parse_data(self.__get_variables("risk_factors"), risk_atrial_fib))

        return patient

    def __create_onset(self) -> Onset:
        """Creates the Onset part of MedicalReport

        Returns
        -------
        Onset
            The onset part medical report with all the template values yet to be replaced
        """

        onset_data = OnsetData.from_dict(self.data)

        onset = Onset(onset_data.onset_timestamp,
                      onset_data.wake_up_stroke,
                      self.__get_setting("date_format"),
                      self.__get_setting("time_format"))

        return onset

    def __create_admission(self) -> Admission:
        """Creates the Admission part of MedicalReport

        Returns
        -------
        Admission
            The admission part medical report with all the template values yet to be replaced
        """

        admission_data = AdmissionData.from_dict(self.data)

        admission = Admission(admission_data.nihss_score, admission_data.aspects_score,
                              admission_data.hospitalized_in,
                              admission_data.prestroke_mrs,
                              admission_data.sys_blood_pressure,
                              admission_data.dia_blood_pressure,
                              admission_data.hospital_timestamp,
                              admission_data.arrival_mode,
                              admission_data.department_type,
                              admission_data.prenotification,
                              self.__get_setting("time_format"))

        return admission

    def __create_treatment(self) -> Treatment:
        """Creates the Treatment part of MedicalReport. Includes both Thrombolysis and Thrombectomy

        Returns
        -------
        Treatment
            The treatment part medical report with all the template values yet to be replaced
        """

        treatment_data = TreatmentData.from_dict(self.data)
        thrombolysis = Thrombolysis(treatment_data.dtn,
                                    treatment_data.ivt_treatment,
                                    treatment_data.ivt_dose)

        tici_score_meaning_val = None

        if treatment_data.tici_score is not None and treatment_data.tici_score != "occlusion not confirmed":
            tici_score_meaning_val = f"tici_score_{treatment_data.tici_score}"

        thrombectomy = Thrombectomy(treatment_data.dtg, treatment_data.tici_score, treatment_data.dio,
                                    tici_score_meaning_val)

        self.transported = thrombectomy.thrombectomy_transport

        treatment = Treatment(treatment_data.thrombolysis, treatment_data.thrombectomy,
                              treatment_data.no_thrombolysis_reason,
                              treatment_data.no_thrombectomy_reason,
                              thrombolysis, thrombectomy)

        return treatment

    def __create_follow_up_imaging(self) -> Optional[FollowUpImaging]:
        """Creates the FollowUpImaging part of MedicalReport

        Returns
        -------
        FollowUpImaging
            The follow-up imaging part medical report with all the template values yet to be replaced.
            If the patient was transported and therefore no follow-up imaging could be performed

        """

        if self.transported:
            return None

        imaging_data = ImagingData.from_dict(self.data)
        imaging_treatment_data = ImagingTreatmentData.from_dict(self.data)

        imaging = FollowUpImaging(self.__parse_data(
            self.__get_variables("post_treatment_findings"), vars(imaging_treatment_data)),
            imaging_data.imaging_type)

        return imaging

    def __create_post_acute_care(self) -> Optional[PostAcuteCare]:
        """Creates the PostAcuteCare part of MedicalReport

        Returns
        -------
        PostAcuteCare
            The post acute care part medical report with all the template values yet to be replaced.
            If the patient was transported and therefore no post acute care could be performed

        """

        if self.transported:
            return None

        post_acute_care_data = PostAcuteCareData.from_dict(self.data)

        post_acute_care = PostAcuteCare(post_acute_care_data.afib_flutter,
                                        post_acute_care_data.swallowing_screening,
                                        post_acute_care_data.swallowing_screening_type,
                                        post_acute_care_data.physiotherapy_received,
                                        post_acute_care_data.occup_physiotherapy_received,
                                        post_acute_care_data.speech_therapy_received,
                                        None)

        post_acute_care_therapies = {"physiotherapy": post_acute_care.physiotherapy,
                                     "ergotherapy": post_acute_care.ergotherapy,
                                     "speechtherapy": post_acute_care.speechtherapy}

        post_acute_care.therapies = self.__parse_data(self.__get_variables("therapies"), post_acute_care_therapies)

        return post_acute_care

    def __create_post_stroke_complications(self) -> PostStrokeComplications:
        """Creates the PostStrokeComplications part of MedicalReport

        Returns
        -------
        PostStrokeComplications
            The post stroke complications part medical report with all the template values yet to be replaced

        """

        post_stroke_complications_data = PostStrokeComplicationsData.from_dict(self.data)

        post_stroke_complications = PostStrokeComplications(self.__parse_data(
            self.__get_variables("post_stroke_complications"), vars(post_stroke_complications_data)))

        return post_stroke_complications

    def __create_etiology(self) -> Optional[Etiology]:
        """Creates the Etiology part of MedicalReport. Includes LargeArteryAtherosclerosis and Cardioembolism

        Returns
        -------
        Etiology
            The etiology part medical report with all the template values yet to be replaced.
            If the patient was transported and therefore no etiology could be performed

        """

        if self.transported:
            return None

        etiology_data = EtiologyData.from_dict(self.data)

        etiology = Etiology(etiology_data.etiology_large_artery, etiology_data.etiology_cardioembolism,
                            etiology_data.etiology_other, etiology_data.etiology_cryptogenic_stroke,
                            etiology_data.etiology_small_vessel, etiology_data.carotid_stenosis,
                            etiology_data.carotid_stenosis_level, etiology_data.afib_flutter)

        return etiology

    def __create_discharge(self) -> Discharge:
        """Creates the Discharge part of MedicalReport

        Returns
        -------
        Discharge
            The discharge part medical report with all the template values yet to be replaced.

        """
        discharge_data = DischargeData.from_dict(self.data)
        medication_data = MedicationData.from_dict(self.data)

        discharge = Discharge(discharge_data.discharge_date,
                              discharge_data.discharge_destination,
                              discharge_data.nihss,
                              discharge_data.discharge_mrs,
                              discharge_data.contact_date,
                              discharge_data.mode_contact,
                              self.__parse_data(self.__get_variables("medications"), vars(medication_data)),
                              self.__get_setting("date_format"))

        return discharge

    def __get_variables(self, key: str) -> Optional[dict]:
        """Gets the 'variables' sub dictionary from the dictionary

        Parameters
        ----------
        key : str
            Key of the sub dictionary to be returned

        Returns
        -------
        dict
            The sub dictionary specified by the key. None if the key is incorrect

        Raises
        ------
        KeyError
            If the dictionary is missing given key

        """

        try:
            variable = self.language.variables[key]
        except KeyError:
            logging.error("Variables are missing key %s", key)
            return None

        return variable

    def __get_setting(self, key: str) -> Optional[str]:
        """Gets the specified setting from the dictionary

        Parameters
        ----------
        key :
            Key of the setting to be returned.

        Returns
        -------
            The setting specified by the key. None if the key is incorrect

        Raises
        ------
        KeyError
            If the dictionary is missing given key

        """

        try:
            setting = self.language.settings[key]
        except KeyError:
            logging.error("Settings are missing key %s", key)
            return None

        return setting

    @staticmethod
    def __prepare_scoped_values(values: dict) -> dict:
        """Prepares the values as scoped values for substitution. Concatenating the keys of parent dictionary with the
        keys of the children dictionaries.

        Parameters
        ----------
        values : dict
            The parent dictionary with values to be concatenated

        Returns
        -------
        dict
            The concatenated values

        """

        scoped_values = {}

        for key, vals in values.items():
            for val_key, val_value in vals.items():
                scoped_key = f"{key}.{val_key}"
                scoped_values[scoped_key] = val_value

        return scoped_values

    @staticmethod
    def __translate_data(dictionary: dict, key: str) -> str:
        """Translates the data specified by key with the values from dictionary

        Parameters
        ----------
        dictionary : dict
            Dictionary used for the translation
        key : str
            The key for the value from data dictionary that is to be translated

        Returns
        -------
        str
            Translated value
        """

        if dictionary is None:
            return ""

        if key:
            try:
                variable = dictionary[key]
            except KeyError:
                logging.error("Invalid key %s", key)
                variable = ""

            return variable

        return ""

    def __parse_data(self, dictionary: dict, data: dict) -> str:
        """Parses the variables from dictionary specified by the data

        Parameters
        ----------
        dictionary : dict
            A dictionary from which the text versions are taken from
        data : dict
            A dictionary with the data to be parsed

        Returns
        -------
        str
            The resulting parsed text from json dictionary based on the data
        """

        result = ""
        if dictionary is None:
            return result

        for key, value in data.items():
            if value:
                variable = ""

                try:
                    variable = dictionary[key]
                except KeyError:
                    logging.error("Invalid key %s", key)

                if variable != "":
                    result += variable if result == "" else f", {variable}"

        result = self.replace_last(result, ",", ", and")

        return result

    @staticmethod
    def replace_last(string: str, old: str, new: str) -> str:
        """Replaces the last substring with new substring of given string

        Parameters
        ----------
        string : str
            The string in which we are replacing substrings
        old : str
            The last occurrence of the string to be replaced
        new : str
            The replacement string

        Returns
        -------
        str
            The replaced string
        """

        return new.join(string.rsplit(old, 1))

    def __translate_variables(self, mr: MedicalReport) -> dict:
        """Translates the variables in the discharge report

        Returns
        -------
        dict
            Dictionary of the medical discharge report with translated values
        """

        # Diagnosis
        mr.diagnosis.imaging_type = self.__translate_data(self.__get_variables("imaging_type"), mr.diagnosis.imaging_type)

        # Patient
        mr.patient.sex = self.__translate_data(self.__get_variables("sex"), mr.patient.sex)

        # Admission
        mr.admission.admission_type = self.__translate_data(self.__get_variables("admission_type"),
                                                            mr.admission.admission_type)
        mr.admission.arrival_mode = self.__translate_data(self.__get_variables("arrival_mode"), mr.admission.arrival_mode)
        mr.admission.department_type = self.__translate_data(self.__get_variables("department_type"),
                                                             mr.admission.department_type)

        # Treatment
        mr.treatment.thrombolysis.ivt_treatment = self.__translate_data(self.__get_variables("ivt_treatment"),
                                                                        mr.treatment.thrombolysis.ivt_treatment)
        mr.treatment.no_thrombolysis_reasons = self.__translate_data(self.__get_variables("no_thrombolysis_reason"),
                                                                     mr.treatment.no_thrombolysis_reasons)
        mr.treatment.no_thrombectomy_reasons = self.__translate_data(self.__get_variables("no_thrombectomy_reason"),
                                                                     mr.treatment.no_thrombectomy_reasons)
        mr.treatment.thrombectomy.tici_score_meaning = self.__translate_data(self.__get_variables("tici_score_meaning"),
                                                                             mr.treatment.thrombectomy.tici_score_meaning)

        # Post acute care
        if not self.transported:
            mr.post_acute_care.swallowing_screening_type = \
                self.__translate_data(self.__get_variables("swallowing_screening_type"),
                                      mr.post_acute_care.swallowing_screening_type)

        # Discharge
        mr.discharge.discharge_destination = self.__translate_data(self.__get_variables("discharge_destination"),
                                                                   mr.discharge.discharge_destination)

        return mr.to_dict()
