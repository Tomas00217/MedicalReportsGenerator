import logging
import copy
from string import Template
from typing import Any, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.language import Language
from data.data_objects import DiagnosisData, OnsetData, AdmissionData, TreatmentData, \
    PostAcuteCareData, PostStrokeComplicationsData, EtiologyData, DischargeData, MedicationData, \
    DiagnosisOcclusionsData, ImagingTreatmentData, RiskFactorsData, PriorTreatmentData, PatientData
from data.models import Diagnosis, Onset, Admission, Thrombolysis, Thrombectomy, Treatment, \
    PostAcuteCare, PostStrokeComplications, Etiology, LargeArteryAtherosclerosis, Cardioembolism, \
    Discharge, MedicalRecord, Patient


class MyTemplate(Template):
    """
    Class representing a Template with custom pattern

    """
    idpattern = r'(?-i:[._a-zA-Z][._a-zA-Z0-9]*)'


class MedicalRecordsGenerator:
    """
    A class representing the medical record generator.

    Serves to generate the medical record piece by piece.

    Methods
    -------
    generate_medical_record()
        Loads the jinja2 template and renders the template with generated structure
    generate_structure()
        Generates the whole structure of a medical record
    create_structure()
        Creates the whole MedicalRecord from all of its parts
    create_diagnosis()
        Creates the Diagnosis part of MedicalRecord
    create_onset()
        Creates the Onset part of MedicalRecord
    create_admission()
        Creates the Admission part of MedicalRecord
    create_treatment()
        Creates the Treatment part of MedicalRecord
    create_follow_up_imaging()
        Creates the FollowUpImaging part of MedicalRecord
    create_post_acute_care()
        Creates the PostAcuteCare part of MedicalRecord
    create_post_stroke_complications()
        Creates the PostStrokeComplications part of MedicalRecord
    create_etiology()
        Creates the Etiology part of MedicalRecord
    create_discharge()
        Creates the Discharge part of MedicalRecord
    create_diagnosis()
        Creates the Diagnosis part of MedicalRecord
    create_diagnosis()
        Creates the Diagnosis part of MedicalRecord
    create_diagnosis()
        Creates the Diagnosis part of MedicalRecord
    get_variables()
        Gets the 'variables' sub dictionary from the dictionary
    get_setting()
        Gets the specified setting from the dictionary
    prepare_scoped_values()
        Prepares the values as scoped values for substitution
    translate_data(dictionary, key)
        Translates the data specified by key with the values from dictionary
    parse_data(dictionary, data)
        Parses the variables from dictionary specified by the data
    replace_last(string, old, new)
        Replaces the last substring with new substring of given string
    get_tici_meaning(dictionary, tici_score)
        Gets the tici meaning based on the tici score
    translate_variables()
        Translates the variables in the discharge report

    """

    def __init__(self, language: Language, data: Any):
        """

        Parameters
        ----------
        language : Language
            Loaded language variant of the dictionary
        data : Any
            Data from the database
        """

        self.language = language
        self.data = data
        self.transported = False
        self.medical_record = self.create_medical_record()

    def generate_medical_record(self) -> str:
        """Loads the jinja2 template and renders the template with generated structure

        Returns
        -------
        str
            Generated medical record with all the values substituted
        """

        env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
        template = env.get_template("main.txt")

        record = self.generate_structure()

        return template.render(record=record)

    def generate_structure(self) -> dict:
        """Generates the whole structure of a medical record with replaced string template values

        Returns
        -------
        dict
            Medical record as a dict to be used for jinja2 template
        """

        # We create a deep copy of dictionary with variables from medical record for the purpose of condition evaluation
        # while parsing, these variables are then translated and used for substitution
        variables = copy.deepcopy(self.medical_record.to_dict())
        translations = self.translate_variables()
        scoped_values = self.prepare_scoped_values(translations)

        record = {
            "diagnosis": MyTemplate(self.language.diagnosis.get_block_result(variables)
                                    if self.medical_record.diagnosis else "").safe_substitute(scoped_values),

            "patient": MyTemplate(self.language.patient.get_block_result(variables)
                                  if self.medical_record.patient else "").safe_substitute(scoped_values),

            "onset": MyTemplate(self.language.onset.get_block_result(variables)
                                if self.medical_record.onset else "").safe_substitute(scoped_values),

            "admission": MyTemplate(self.language.admission.get_block_result(variables)
                                    if self.medical_record.admission else "").safe_substitute(scoped_values),

            "treatment": MyTemplate(self.language.treatment.get_block_result(variables)
                                    if self.medical_record.treatment else "").safe_substitute(scoped_values),

            # "follow_up_imaging": MyTemplate(self.language.follow_up_imaging.get_block_result(variables)
            #                                 if self.medical_record.follow_up_imaging else "")
            # .safe_substitute(scoped_values),

            "post_acute_care": MyTemplate(self.language.post_acute_care.get_block_result(variables)
                                          if self.medical_record.post_acute_care else "")
            .safe_substitute(scoped_values),

            "post_stroke_complications": MyTemplate(self.language.post_stroke_complications.get_block_result(variables)
                                                    if self.medical_record.post_stroke_complications else "")
            .safe_substitute(scoped_values),

            "etiology": MyTemplate(self.language.etiology.get_block_result(variables)
                                   if self.medical_record.etiology else "").safe_substitute(scoped_values),

            "discharge": MyTemplate(self.language.discharge.get_block_result(variables)
                                    if self.medical_record.discharge else "").safe_substitute(scoped_values),
        }

        return record

    def create_medical_record(self) -> MedicalRecord:
        """Creates the whole MedicalRecord from all of its parts

        Returns
        -------
        MedicalRecord
            The whole medical record with all the template values yet to be replaced
        """

        return MedicalRecord(self.create_diagnosis(),
                             self.create_patient(),
                             self.create_onset(),
                             self.create_admission(),
                             self.create_treatment(),
                             # self.create_follow_up_imaging(),
                             self.create_post_acute_care(),
                             self.create_post_stroke_complications(),
                             self.create_etiology(),
                             self.create_discharge())

    def create_diagnosis(self) -> Diagnosis:
        """Creates the Diagnosis part of MedicalRecord

        Returns
        -------
        Diagnosis
            The diagnosis part medical record with all the template values yet to be replaced
        """

        diagnosis_data = DiagnosisData.from_dict(self.data)
        diagnosis_occlusions = DiagnosisOcclusionsData.from_dict(self.data)

        diagnosis = Diagnosis(diagnosis_data.stroke_type,
                              diagnosis_data.aspects_score,
                              diagnosis_data.imaging_type,
                              self.parse_data(self.get_variables("occlusion_position"), vars(diagnosis_occlusions)),
                              diagnosis_data.imaging_timestamp,
                              diagnosis_data.imaging_within_hour,
                              self.get_setting("time_format"))

        return diagnosis

    def create_patient(self) -> Patient:
        """Creates the Patient part of MedicalRecord

        Returns
        -------
        Patient
            The patient part medical record with all the template values yet to be replaced
        """

        patient_data = PatientData.from_dict(self.data)
        risk_factors_data = RiskFactorsData.from_dict(self.data)
        prior_treatment_data = PriorTreatmentData.from_dict(self.data)
        risk_atrial_fib = {"risk_atrial_fibrilation": patient_data.risk_atrial_fibrilation}

        patient = Patient(patient_data.patient_id,
                          patient_data.age,
                          patient_data.sex,
                          self.parse_data(self.get_variables("risk_factors"), vars(risk_factors_data)),
                          self.parse_data(self.get_variables("prior_treatment"), vars(prior_treatment_data)),
                          self.parse_data(self.get_variables("risk_factors"), risk_atrial_fib))

        return patient

    def create_onset(self) -> Onset:
        """Creates the Onset part of MedicalRecord

        Returns
        -------
        Onset
            The onset part medical record with all the template values yet to be replaced
        """

        onset_data = OnsetData.from_dict(self.data)

        onset = Onset(onset_data.onset_timestamp,
                      onset_data.wake_up_stroke,
                      self.get_setting("date_format"),
                      self.get_setting("time_format"))

        return onset

    def create_admission(self) -> Admission:
        """Creates the Admission part of MedicalRecord

        Returns
        -------
        Admission
            The admission part medical record with all the template values yet to be replaced
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
                              self.get_setting("time_format"))

        return admission

    def create_treatment(self) -> Treatment:
        """Creates the Treatment part of MedicalRecord. Includes both Thrombolysis and Thrombectomy

        Returns
        -------
        Treatment
            The treatment part medical record with all the template values yet to be replaced
        """

        treatment_data = TreatmentData.from_dict(self.data)
        thrombolysis = Thrombolysis(treatment_data.dtn,
                                    treatment_data.ivt_treatment,
                                    treatment_data.ivt_dose)

        thrombectomy = Thrombectomy(treatment_data.dtg, treatment_data.tici_score, treatment_data.dio,
                                    self.get_tici_meaning(self.get_variables("tici_score_meaning"),
                                                          treatment_data.tici_score))

        self.transported = thrombectomy.thrombectomy_transport

        treatment = Treatment(treatment_data.thrombolysis, treatment_data.thrombectomy,
                              treatment_data.no_thrombolysis_reason,
                              treatment_data.no_thrombectomy_reason,
                              thrombolysis, thrombectomy)

        return treatment

    # def create_follow_up_imaging(self) -> Optional[FollowUpImaging]:
    #     """Creates the FollowUpImaging part of MedicalRecord
    #
    #     Returns
    #     -------
    #     FollowUpImaging
    #         The follow-up imaging part medical record with all the template values yet to be replaced.
    #         If the patient was transported and therefore no follow-up imaging could be performed
    #
    #     """
    #
    #     if self.transported:
    #         return None
    #
    #     imaging_data = ImagingData.from_dict(self.data)
    #     imaging_treatment_data = ImagingTreatmentData.from_dict(self.data)
    #
    #     imaging = FollowUpImaging(self.parse_data(
    #         self.get_variables("post_treatment_findings"), vars(imaging_treatment_data)),
    #         imaging_data.imaging_type)
    #
    #     return imaging

    def create_post_acute_care(self) -> Optional[PostAcuteCare]:
        """Creates the PostAcuteCare part of MedicalRecord

        Returns
        -------
        PostAcuteCare
            The post acute care part medical record with all the template values yet to be replaced.
            If the patient was transported and therefore no post acute care could be performed

        """

        if self.transported:
            return None

        post_acute_care_data = PostAcuteCareData.from_dict(self.data)
        imaging_treatment_data = ImagingTreatmentData.from_dict(self.data)

        post_acute_care = PostAcuteCare(post_acute_care_data.afib_flutter,
                                        self.parse_data(self.get_variables("post_treatment_findings"),
                                                        vars(imaging_treatment_data)),
                                        post_acute_care_data.imaging_type,
                                        post_acute_care_data.swallowing_screening,
                                        post_acute_care_data.swallowing_screening_type,
                                        post_acute_care_data.physiotherapy_received,
                                        post_acute_care_data.occup_physiotherapy_received,
                                        post_acute_care_data.speech_therapy_received,
                                        None)

        post_acute_care_therapies = {"physiotherapy": post_acute_care.physiotherapy,
                                     "ergotherapy": post_acute_care.ergotherapy,
                                     "speechtherapy": post_acute_care.speechtherapy}

        post_acute_care.therapies = self.parse_data(self.get_variables("therapies"), post_acute_care_therapies)

        return post_acute_care

    def create_post_stroke_complications(self) -> PostStrokeComplications:
        """Creates the PostStrokeComplications part of MedicalRecord

        Returns
        -------
        PostStrokeComplications
            The post stroke complications part medical record with all the template values yet to be replaced

        """

        post_stroke_complications_data = PostStrokeComplicationsData.from_dict(self.data)

        post_stroke_complications = PostStrokeComplications(self.parse_data(
            self.get_variables("post_stroke_complications"), vars(post_stroke_complications_data)))

        return post_stroke_complications

    def create_etiology(self) -> Optional[Etiology]:
        """Creates the Etiology part of MedicalRecord. Includes LargeArteryAtherosclerosis and Cardioembolism

        Returns
        -------
        Etiology
            The etiology part medical record with all the template values yet to be replaced.
            If the patient was transported and therefore no etiology could be performed

        """

        if self.transported:
            return None

        etiology_data = EtiologyData.from_dict(self.data)

        large_artery = LargeArteryAtherosclerosis(etiology_data.carotid_stenosis,
                                                  etiology_data.carotid_stenosis_level,
                                                  etiology_data.carotid_stenosis_followup)

        cardioembolism = Cardioembolism(etiology_data.afib_flutter, None)
        if cardioembolism.afib_flutter is not None:
            cardioembolism.reasons = "atrial fibrilation/flutter"

        etiology = Etiology(etiology_data.etiology_large_artery, etiology_data.etiology_cardioembolism,
                            etiology_data.etiology_other, etiology_data.etiology_cryptogenic_stroke,
                            etiology_data.etiology_small_vessel, large_artery, cardioembolism)

        return etiology

    def create_discharge(self) -> Discharge:
        """Creates the Discharge part of MedicalRecord

        Returns
        -------
        Discharge
            The discharge part medical record with all the template values yet to be replaced.

        """
        discharge_data = DischargeData.from_dict(self.data)
        medication_data = MedicationData.from_dict(self.data)

        discharge = Discharge(discharge_data.discharge_date,
                              discharge_data.discharge_destination,
                              discharge_data.nihss,
                              discharge_data.discharge_mrs,
                              discharge_data.contact_date,
                              discharge_data.mode_contact,
                              self.parse_data(self.get_variables("medications"), vars(medication_data)),
                              self.get_setting("date_format"))

        return discharge

    def get_variables(self, key: str) -> Optional[dict]:
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

    def get_setting(self, key: str) -> Optional[str]:
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
    def prepare_scoped_values(values: dict) -> dict:
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
    def translate_data(dictionary: dict, key: str) -> str:
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

    def parse_data(self, dictionary: dict, data: dict) -> str:
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

    @staticmethod
    def get_tici_meaning(dictionary: dict, tici_score: str) -> str:
        """Gets the tici meaning based on the tici score

        Parameters
        ----------
        dictionary : dict
            Dictionary from which the text is being taken
        tici_score : str
            Tici score of patient

        Returns
        -------
        str
            Parsed tici meaning based on the tici score

        """

        if dictionary is None:
            return ""

        if tici_score is not None and tici_score != "occlusion not confirmed":
            tici_score = tici_score
            return dictionary[f"tici_score_{tici_score}"]

    def translate_variables(self) -> dict:
        """Translates the variables in the discharge report

        Returns
        -------
        dict
            Dictionary of the medical discharge report with translated values
        """

        mr = self.medical_record

        # Diagnosis
        mr.diagnosis.imaging_type = self.translate_data(self.get_variables("imaging_type"), mr.diagnosis.imaging_type)

        # Patient
        mr.patient.sex = self.translate_data(self.get_variables("sex"), mr.patient.sex)

        # Admission
        mr.admission.admission_type = self.translate_data(self.get_variables("hospitalized_in"),
                                                          mr.admission.admission_type)
        mr.admission.arrival_mode = self.translate_data(self.get_variables("arrival_mode"), mr.admission.arrival_mode)
        mr.admission.department_type = self.translate_data(self.get_variables("department_type"),
                                                           mr.admission.department_type)

        # Treatment
        mr.treatment.thrombolysis.ivt_treatment = self.translate_data(self.get_variables("ivt_treatment"),
                                                                      mr.treatment.thrombolysis.ivt_treatment)
        mr.treatment.thrombolysis_reasons = self.translate_data(self.get_variables("no_thrombolysis_reason"),
                                                                mr.treatment.thrombolysis_reasons),
        mr.treatment.thrombectomy_reasons = self.translate_data(self.get_variables("no_thrombectomy_reason"),
                                                                mr.treatment.thrombectomy_reasons),

        # Post acute care
        if not self.transported:
            mr.post_acute_care.swallowing_screening_type = \
                self.translate_data(self.get_variables("swallowing_screening_type"),
                                    mr.post_acute_care.swallowing_screening_type),

        # Discharge
        mr.discharge.discharge_destination = self.translate_data(self.get_variables("discharge_destination"),
                                                                 mr.discharge.discharge_destination)

        return self.medical_record.to_dict()
