
from medicalrecordgenerator.data.data_objects import DiagnosisData, OnsetData, AdmissionData, TreatmentData, \
    ImagingData, PostAcuteCareData, PostStrokeComplicationsData, EtiologyData, DischargeData, MedicationData, \
    DiagnosisOcclusionsData, ImagingTreatmentData
from jinja2 import Environment, FileSystemLoader, select_autoescape

from medicalrecordgenerator.data.models import Diagnosis, Onset, Admission, Thrombolysis, Thrombectomy, Treatment, \
    FollowUpImaging, PostAcuteCare, PostStrokeComplications, Etiology, LargeArteryAtherosclerosis, Cardioembolism, \
    Discharge
from medicalrecordgenerator.data.parser_old import parse_data, get_tici_meaning


class MedicalRecordsGenerator:
    def __init__(self, dictionary, data):
        self.dictionary = dictionary
        self.data = data

    # TODO Čo s prekladmi premennych z DB ??
    def generate_medical_record(self):
        env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
        template = env.get_template("main.txt")

        record = self.generate_structure()

        return template.render(record=record)

    def generate_structure(self):
        record = {
            "diagnosis": self.generate_diagnosis(),
            "onset": self.generate_onset(),
            "admission": self.generate_admission(),
            "treatment": self.generate_treatment(),
            "imaging": self.generate_follow_up_imaging(),
            "post_acute_care": self.generate_post_acute_care(),
            "post_stroke_complications": self.generate_post_stroke_complications(),
            "etiology": self.generate_etiology(),
            "discharge": self.generate_discharge()
        }

        return record

    def generate_diagnosis(self):
        diagnosis_data = DiagnosisData.from_dict(self.data)
        diagnosis_occlusions = DiagnosisOcclusionsData.from_dict(self.data)
        variables = self.dictionary["variables"]["occlusion_position"]

        diagnosis = Diagnosis(diagnosis_data.stroke_type,
                              diagnosis_data.aspects_score,
                              diagnosis_data.imaging_type,
                              parse_data(variables, diagnosis_occlusions))

        return diagnosis.generate(self.dictionary["diagnosis"])

    def generate_onset(self):
        onset_data = OnsetData.from_dict(self.data)
        settings = self.dictionary["settings"]

        onset = Onset(onset_data.onset_timestamp,
                      onset_data.wake_up_stroke,
                      settings["date_format"])

        return onset.generate(self.dictionary["onset"])

    def generate_admission(self):
        admission_data = AdmissionData.from_dict(self.data)
        admission = Admission(admission_data.nihss_score, admission_data.hospitalized_in)

        return admission.generate(self.dictionary["admission"])

    def generate_treatment(self):
        treatment_data = TreatmentData.from_dict(self.data)
        variables = self.dictionary["variables"]["tici_score_meaning"]
        thrombolysis = Thrombolysis(treatment_data.dtn, treatment_data.ivt_treatment, treatment_data.ivt_dose)
        thrombectomy = Thrombectomy(treatment_data.dtg, treatment_data.tici_score, treatment_data.dio,
                                    get_tici_meaning(variables, treatment_data.tici_score))

        treatment = Treatment(treatment_data.thrombolysis, treatment_data.thrombectomy,
                              treatment_data.no_thrombolysis_reason, treatment_data.no_thrombectomy_reason,
                              thrombolysis, thrombectomy)

        return treatment.generate(self.dictionary["treatment"])

    def generate_follow_up_imaging(self):
        imaging_data = ImagingData.from_dict(self.data)
        imaging_treatment_data = ImagingTreatmentData.from_dict(self.data)

        variables = self.dictionary["variables"]["post_treatment_findings"]

        imaging = FollowUpImaging(parse_data(variables, imaging_treatment_data),
                                  imaging_data.imaging_type,
                                  imaging_data.aspects_score)

        return imaging.generate(self.dictionary["follow_up_imaging"])

    def generate_post_acute_care(self):
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

        post_acute_care.therapies = parse_data(variables, post_acute_care_therapies)

        return post_acute_care.generate(self.dictionary["post_acute_care"])

    def generate_post_stroke_complications(self):
        post_stroke_complications_data = PostStrokeComplicationsData.from_dict(self.data)
        variables = self.dictionary["variables"]["post_stroke_complications"]

        post_stroke_complications = PostStrokeComplications(parse_data(variables, post_stroke_complications_data))

        return post_stroke_complications.generate(self.dictionary["post_stroke_complications"])

    def generate_etiology(self):
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

        return etiology.generate(self.dictionary["etiology"])

    def generate_discharge(self):
        discharge_data = DischargeData.from_dict(self.data)
        medication_data = MedicationData.from_dict(self.data)

        variables = self.dictionary["variables"]["medications"]
        settings = self.dictionary["settings"]

        discharge = Discharge(discharge_data.discharge_date, discharge_data.discharge_destination,
                              discharge_data.nihss, discharge_data.mrs, discharge_data.contact_date,
                              discharge_data.mode_contact, parse_data(variables, medication_data),
                              settings["date_format"])

        return discharge.generate(self.dictionary["discharge"])
