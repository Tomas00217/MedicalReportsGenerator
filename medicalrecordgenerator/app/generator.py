import logging
from string import Template
from typing import Any, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from .parser import Parser
from data.data_objects import DiagnosisData, OnsetData, AdmissionData, TreatmentData, \
    ImagingData, PostAcuteCareData, PostStrokeComplicationsData, EtiologyData, DischargeData, MedicationData, \
    DiagnosisOcclusionsData, ImagingTreatmentData
from data.models import Diagnosis, Onset, Admission, Thrombolysis, Thrombectomy, Treatment, \
    FollowUpImaging, PostAcuteCare, PostStrokeComplications, Etiology, LargeArteryAtherosclerosis, Cardioembolism, \
    Discharge, MedicalRecord


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

    """

    def __init__(self, dictionary: dict, data: Any):
        """

        Parameters
        ----------
        dictionary : dict
            Loaded language variant of the dictionary
        data : Any
            Data from the database
        """

        self.dictionary = dictionary
        self.data = data
        self.transported = False
        self.parser = Parser({})
        try:
            self.variables = dictionary["variables"]
        except KeyError:
            logging.error("Dictionary is missing key 'variables'")
            self.variables = {}

        try:
            self.settings = dictionary["settings"]
        except KeyError:
            logging.error("Dictionary is missing key 'settings'")
            self.settings = {}

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

        variables = self.medical_record.to_dict()
        self.parser.data = variables

        scoped_values = self.prepare_scoped_values(variables)

        record = {
            "diagnosis": MyTemplate(self.medical_record.diagnosis.get_text(self.dictionary["diagnosis"], self.parser)
                                    if self.medical_record.diagnosis else "").safe_substitute(scoped_values),

            "onset": MyTemplate(self.medical_record.onset.get_text(self.dictionary["onset"], self.parser)
                                if self.medical_record.onset else "").safe_substitute(scoped_values),

            "admission": MyTemplate(self.medical_record.admission.get_text(self.dictionary["admission"], self.parser)
                                    if self.medical_record.admission else "").safe_substitute(scoped_values),

            "treatment": MyTemplate(self.medical_record.treatment.get_text(self.dictionary["treatment"], self.parser)
                                    if self.medical_record.treatment else "").safe_substitute(scoped_values),

            "follow_up_imaging": MyTemplate(
                self.medical_record.follow_up_imaging.get_text(self.dictionary["follow_up_imaging"],
                                                               self.parser)
                if self.medical_record.follow_up_imaging else "").safe_substitute(scoped_values),

            "post_acute_care": MyTemplate(
                self.medical_record.post_acute_care.get_text(self.dictionary["post_acute_care"],
                                                             self.parser)
                if self.medical_record.post_acute_care else "").safe_substitute(scoped_values),

            "post_stroke_complications": MyTemplate(self.medical_record.post_stroke_complications
                                                    .get_text(self.dictionary["post_stroke_complications"], self.parser)
                                                    if self.medical_record.post_stroke_complications else "")
            .safe_substitute(scoped_values),

            "etiology": MyTemplate(self.medical_record.etiology.get_text(self.dictionary["etiology"], self.parser)
                                   if self.medical_record.etiology else "").safe_substitute(scoped_values),

            "discharge": MyTemplate(self.medical_record.discharge.get_text(self.dictionary["discharge"], self.parser)
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
                             self.create_onset(),
                             self.create_admission(),
                             self.create_treatment(),
                             self.create_follow_up_imaging(),
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
                              self.parser.translate_data(self.get_variables("imaging_type"),
                                                         diagnosis_data.imaging_type),
                              self.parser.parse_data(self.get_variables("occlusion_position"),
                                                     vars(diagnosis_occlusions)))

        return diagnosis

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
                              self.parser.translate_data(self.get_variables("hospitalized_in"),
                                                         admission_data.hospitalized_in))

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
                                    self.parser.translate_data(self.get_variables("ivt_treatment"),
                                                               treatment_data.ivt_treatment),
                                    treatment_data.ivt_dose)

        thrombectomy = Thrombectomy(treatment_data.dtg, treatment_data.tici_score, treatment_data.dio,
                                    self.parser.get_tici_meaning(self.get_variables("tici_score_meaning"),
                                                                 treatment_data.tici_score))

        self.transported = thrombectomy.thrombectomy_transport

        treatment = Treatment(treatment_data.thrombolysis, treatment_data.thrombectomy,
                              self.parser.translate_data(self.get_variables("no_thrombolysis_reason"),
                                                         treatment_data.no_thrombolysis_reason),
                              self.parser.translate_data(self.get_variables("no_thrombectomy_reason"),
                                                         treatment_data.no_thrombectomy_reason),
                              thrombolysis, thrombectomy)

        return treatment

    def create_follow_up_imaging(self) -> Optional[FollowUpImaging]:
        """Creates the FollowUpImaging part of MedicalRecord

        Returns
        -------
        FollowUpImaging
            The follow-up imaging part medical record with all the template values yet to be replaced.
            If the patient was transported and therefore no follow-up imaging could be performed

        """

        if self.transported:
            return None

        imaging_data = ImagingData.from_dict(self.data)
        imaging_treatment_data = ImagingTreatmentData.from_dict(self.data)

        imaging = FollowUpImaging(self.parser.parse_data(self.get_variables("post_treatment_findings"),
                                                         vars(imaging_treatment_data)),
                                  imaging_data.imaging_type)

        return imaging

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

        post_acute_care = PostAcuteCare(post_acute_care_data.dysphagia_screening,
                                        post_acute_care_data.physiotherapy_received,
                                        post_acute_care_data.occup_physiotherapy_received,
                                        post_acute_care_data.speech_therapy_received,
                                        None)

        post_acute_care_therapies = {"physiotherapy": post_acute_care.physiotherapy,
                                     "ergotherapy": post_acute_care.ergotherapy,
                                     "speechtherapy": post_acute_care.speechtherapy}

        post_acute_care.therapies = self.parser.parse_data(self.get_variables("therapies"), post_acute_care_therapies)

        return post_acute_care

    def create_post_stroke_complications(self) -> PostStrokeComplications:
        """Creates the PostStrokeComplications part of MedicalRecord

        Returns
        -------
        PostStrokeComplications
            The post stroke complications part medical record with all the template values yet to be replaced

        """

        post_stroke_complications_data = PostStrokeComplicationsData.from_dict(self.data)

        post_stroke_complications = PostStrokeComplications(self.parser.parse_data(
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
                              self.parser.translate_data(self.get_variables("discharge_destination"),
                                                         discharge_data.discharge_destination),
                              discharge_data.nihss, discharge_data.mrs, discharge_data.contact_date,
                              discharge_data.mode_contact, self.parser.parse_data(self.get_variables("medications"),
                                                                                  vars(medication_data)),
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
            variable = self.variables[key]
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
            setting = self.settings[key]
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
