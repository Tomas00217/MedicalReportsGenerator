from jinja2 import Environment, FileSystemLoader, select_autoescape
from medicalrecordgenerator.app.parser import Parser
from medicalrecordgenerator.data.data_objects import DiagnosisData, OnsetData, AdmissionData, TreatmentData, \
    ImagingData, PostAcuteCareData, PostStrokeComplicationsData, EtiologyData, DischargeData, MedicationData, \
    DiagnosisOcclusionsData, ImagingTreatmentData
from medicalrecordgenerator.data.models import Diagnosis, Onset, Admission, Thrombolysis, Thrombectomy, Treatment, \
    FollowUpImaging, PostAcuteCare, PostStrokeComplications, Etiology, LargeArteryAtherosclerosis, Cardioembolism, \
    Discharge, MedicalRecord


class MedicalRecordsGenerator:
    def __init__(self, dictionary: dict, data: dict):
        self.dictionary = dictionary
        self.data = data
        self.transported = False
        self.parser = Parser({})
        self.medical_record = self.create_medical_record()

    def generate_medical_record(self):
        env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
        template = env.get_template("main.txt")

        record = self.generate_structure()

        return template.render(record=record)

    def generate_structure(self):
        self.parser.data = self.medical_record.to_dict()
        record = {
            "diagnosis": self.medical_record.diagnosis.generate(self.dictionary["diagnosis"], self.parser)
            if self.medical_record.diagnosis else "",

            "onset":  self.medical_record.onset.generate(self.dictionary["onset"], self.parser)
            if self.medical_record.onset else "",

            "admission": self.medical_record.admission.generate(self.dictionary["admission"], self.parser)
            if self.medical_record.admission else "",

            "treatment": self.medical_record.treatment.generate(self.dictionary["treatment"], self.parser)
            if self.medical_record.treatment else "",

            "follow_up_imaging": self.medical_record.follow_up_imaging.generate(self.dictionary["follow_up_imaging"],
                                                                                self.parser)
            if self.medical_record.follow_up_imaging else "",

            "post_acute_care": self.medical_record.post_acute_care.generate(self.dictionary["post_acute_care"],
                                                                            self.parser)
            if self.medical_record.post_acute_care else "",

            "post_stroke_complications": self.medical_record.post_stroke_complications
            .generate(self.dictionary["post_stroke_complications"], self.parser)
            if self.medical_record.post_stroke_complications else "",

            "etiology": self.medical_record.etiology.generate(self.dictionary["etiology"], self.parser)
            if self.medical_record.etiology else "",

            "discharge": self.medical_record.discharge.generate(self.dictionary["discharge"], self.parser)
            if self.medical_record.discharge else ""
        }

        return record

    def create_medical_record(self):
        return MedicalRecord(self.create_diagnosis(),
                             self.create_onset(),
                             self.create_admission(),
                             self.create_treatment(),
                             self.create_follow_up_imaging(),
                             self.create_post_acute_care(),
                             self.create_post_stroke_complications(),
                             self.create_etiology(),
                             self.create_discharge())

    def create_diagnosis(self):
        diagnosis_data = DiagnosisData.from_dict(self.data)
        diagnosis_occlusions = DiagnosisOcclusionsData.from_dict(self.data)
        variables = self.dictionary["variables"]

        diagnosis = Diagnosis(diagnosis_data.stroke_type,
                              diagnosis_data.aspects_score,
                              self.parser.translate_data(variables["imaging_type"], diagnosis_data.imaging_type),
                              self.parser.parse_data(variables["occlusion_position"], diagnosis_occlusions))

        return diagnosis

    def create_onset(self):
        onset_data = OnsetData.from_dict(self.data)
        settings = self.dictionary["settings"]

        onset = Onset(onset_data.onset_timestamp,
                      onset_data.wake_up_stroke,
                      settings["date_format"])

        return onset

    def create_admission(self):
        admission_data = AdmissionData.from_dict(self.data)
        variables = self.dictionary["variables"]
        admission = Admission(admission_data.nihss_score, admission_data.aspects_score,
                              self.parser.translate_data(variables["hospitalized_in"], admission_data.hospitalized_in))

        return admission

    def create_treatment(self):
        treatment_data = TreatmentData.from_dict(self.data)
        variables = self.dictionary["variables"]
        thrombolysis = Thrombolysis(treatment_data.dtn, self.parser.translate_data(variables["ivt_treatment"],
                                                                                   treatment_data.ivt_treatment),
                                    treatment_data.ivt_dose)
        thrombectomy = Thrombectomy(treatment_data.dtg, treatment_data.tici_score, treatment_data.dio,
                                    self.parser.get_tici_meaning(variables["tici_score_meaning"],
                                                                 treatment_data.tici_score))

        self.transported = thrombectomy.thrombectomy_transport

        treatment = Treatment(treatment_data.thrombolysis, treatment_data.thrombectomy,
                              self.parser.translate_data(variables["no_thrombolysis_reason"],
                                                         treatment_data.no_thrombolysis_reason),
                              self.parser.translate_data(variables["no_thrombolysis_reason"],
                                                         treatment_data.no_thrombectomy_reason),
                              thrombolysis, thrombectomy)

        return treatment

    def create_follow_up_imaging(self):
        if self.transported:
            return None

        imaging_data = ImagingData.from_dict(self.data)
        imaging_treatment_data = ImagingTreatmentData.from_dict(self.data)

        variables = self.dictionary["variables"]["post_treatment_findings"]

        imaging = FollowUpImaging(self.parser.parse_data(variables, imaging_treatment_data),
                                  imaging_data.imaging_type)

        return imaging

    def create_post_acute_care(self):
        if self.transported:
            return None

        post_acute_care_data = PostAcuteCareData.from_dict(self.data)
        variables = self.dictionary["variables"]["therapies"]

        post_acute_care = PostAcuteCare(post_acute_care_data.dysphagia_screening,
                                        post_acute_care_data.physiotherapy_received,
                                        post_acute_care_data.occup_physiotherapy_received,
                                        post_acute_care_data.speech_therapy_received,
                                        None)

        post_acute_care_therapies = {"physiotherapy": post_acute_care.physiotherapy,
                                     "ergotherapy": post_acute_care.ergotherapy,
                                     "speechtherapy": post_acute_care.speechtherapy}

        post_acute_care.therapies = self.parser.parse_data(variables, post_acute_care_therapies)

        return post_acute_care

    def create_post_stroke_complications(self):
        post_stroke_complications_data = PostStrokeComplicationsData.from_dict(self.data)
        variables = self.dictionary["variables"]["post_stroke_complications"]

        post_stroke_complications = PostStrokeComplications(self.parser.parse_data(variables,
                                                                                   post_stroke_complications_data))

        return post_stroke_complications

    def create_etiology(self):
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

    def create_discharge(self):
        discharge_data = DischargeData.from_dict(self.data)
        medication_data = MedicationData.from_dict(self.data)

        variables = self.dictionary["variables"]
        settings = self.dictionary["settings"]

        discharge = Discharge(discharge_data.discharge_date,
                              self.parser.translate_data(variables["discharge_destination"],
                                                         discharge_data.discharge_destination),
                              discharge_data.nihss, discharge_data.mrs, discharge_data.contact_date,
                              discharge_data.mode_contact, self.parser.parse_data(variables["medications"],
                                                                                  medication_data),
                              settings["date_format"])

        return discharge
