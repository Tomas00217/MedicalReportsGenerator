
from medicalrecordgenerator.data.data_objects import DiagnosisData, OnsetData, AdmissionData, TreatmentData, \
    ImagingData, PostAcuteCareData, PostStrokeComplicationsData, EtiologyData, DischargeData, MedicationData, \
    DiagnosisOcclusionsData, ImagingTreatmentData
from jinja2 import Environment, FileSystemLoader, select_autoescape

from medicalrecordgenerator.data.models import Diagnosis, Onset, Admission, Thrombolysis, Thrombectomy, Treatment, \
    FollowUpImaging, PostAcuteCare, PostStrokeComplications, Etiology, LargeArteryAtherosclerosis, Cardioembolism, \
    Discharge
from medicalrecordgenerator.data.parser_old import parse_data, get_tici_meaning


# TODO Čo s prekladmi premennych z DB ??
def generate_medical_record(dictionary, data):
    env = Environment(loader=FileSystemLoader("templates"), autoescape=select_autoescape())
    template = env.get_template("main.txt")

    record = generate_structure(dictionary, data)

    return template.render(record=record)


def generate_structure(dictionary, data):
    record = {
        "diagnosis": generate_diagnosis(dictionary, data),
        "onset": generate_onset(dictionary, data),
        "admission": generate_admission(dictionary, data),
        "treatment": generate_treatment(dictionary, data),
        "imaging": generate_follow_up_imaging(dictionary, data),
        "post_acute_care": generate_post_acute_care(dictionary, data),
        "post_stroke_complications": generate_post_stroke_complications(dictionary, data),
        "etiology": generate_etiology(dictionary, data),
        "discharge": generate_discharge(dictionary, data)
    }

    return record


def generate_diagnosis(dictionary, data):
    diagnosis_data = DiagnosisData.from_dict(data)
    diagnosis_occlusions = DiagnosisOcclusionsData.from_dict(data)
    variables = dictionary["variables"]["occlusion_position"]

    diagnosis = Diagnosis(diagnosis_data.stroke_type,
                          diagnosis_data.aspects_score,
                          diagnosis_data.imaging_type,
                          parse_data(variables, diagnosis_occlusions))

    return diagnosis.generate(dictionary["diagnosis"])


def generate_onset(dictionary, data):
    onset_data = OnsetData.from_dict(data)
    settings = dictionary["settings"]

    # TODO: handle time based on locale
    onset_date = onset_data.onset_timestamp.date().strftime(settings["date_format"])
    onset_time = onset_data.onset_timestamp.time()

    onset = Onset(onset_date,
                  onset_time,
                  onset_data.wake_up_stroke)

    return onset.generate(dictionary["onset"])


def generate_admission(dictionary, data):
    admission_data = AdmissionData.from_dict(data)
    admission = Admission(admission_data.nihss_score, admission_data.hospitalized_in)

    return admission.generate(dictionary["admission"])


def generate_treatment(dictionary, data):
    treatment_data = TreatmentData.from_dict(data)
    variables = dictionary["variables"]["tici_score_meaning"]
    thrombolysis = Thrombolysis(treatment_data.dtn, treatment_data.ivt_treatment, treatment_data.ivt_dose)
    thrombectomy = Thrombectomy(treatment_data.dtg, treatment_data.tici_score, treatment_data.dio,
                                get_tici_meaning(variables, treatment_data.tici_score))

    treatment = Treatment(treatment_data.thrombolysis, treatment_data.thrombectomy,
                          treatment_data.no_thrombolysis_reason, treatment_data.no_thrombectomy_reason,
                          thrombolysis, thrombectomy)

    return treatment.generate(dictionary["treatment"])


def generate_follow_up_imaging(dictionary, data):
    imaging_data = ImagingData.from_dict(data)
    imaging_treatment_data = ImagingTreatmentData.from_dict(data)

    variables = dictionary["variables"]["post_treatment_findings"]

    imaging = FollowUpImaging(parse_data(variables, imaging_treatment_data),
                              imaging_data.imaging_type,
                              imaging_data.aspects_score)

    return imaging.generate(dictionary["follow_up_imaging"])


def generate_post_acute_care(dictionary, data):
    post_acute_care_data = PostAcuteCareData.from_dict(data)
    variables = dictionary["variables"]["therapies"]

    post_acute_care = PostAcuteCare(post_acute_care_data.dysphagia_screening,
                                    post_acute_care_data.physiotherapy_received,
                                    post_acute_care_data.occup_physiotherapy_received,
                                    post_acute_care_data.speech_therapy_received,
                                    None)

    post_acute_care_therapies = {"physiotherapy": post_acute_care.physiotherapy,
                                 "ergotherapy": post_acute_care.ergotherapy,
                                 "speechtherapy": post_acute_care.speechtherapy}

    post_acute_care.therapies = parse_data(variables, post_acute_care_therapies)

    return post_acute_care.generate(dictionary["post_acute_care"])


def generate_post_stroke_complications(dictionary, data):
    post_stroke_complications_data = PostStrokeComplicationsData.from_dict(data)
    variables = dictionary["variables"]["post_stroke_complications"]

    post_stroke_complications = PostStrokeComplications(parse_data(variables, post_stroke_complications_data))

    return post_stroke_complications.generate(dictionary["post_stroke_complications"])


def generate_etiology(dictionary, data):
    etiology_data = EtiologyData.from_dict(data)

    large_artery = LargeArteryAtherosclerosis(etiology_data.carotid_stenosis,
                                              etiology_data.carotid_stenosis_level,
                                              etiology_data.carotid_stenosis_followup)

    cardioembolism = Cardioembolism(etiology_data.afib_flutter, None)
    if cardioembolism.afib_flutter is not None:
        cardioembolism.reasons = "atrial fibrilation/flutter"

    etiology = Etiology(etiology_data.etiology_large_artery, etiology_data.etiology_cardioembolism,
                        etiology_data.etiology_other, etiology_data.etiology_cryptogenic_stroke,
                        etiology_data.etiology_small_vessel, large_artery, cardioembolism)

    return etiology.generate(dictionary["etiology"])


def generate_discharge(dictionary, data):
    discharge_data = DischargeData.from_dict(data)
    medication_data = MedicationData.from_dict(data)

    variables = dictionary["variables"]["medications"]

    discharge = Discharge(discharge_data.discharge_date, discharge_data.discharge_destination,
                          discharge_data.nihss, discharge_data.mrs, discharge_data.contact_date,
                          discharge_data.mode_contact, parse_data(variables, medication_data))

    return discharge.generate(dictionary["discharge"])
