from datetime import datetime, time

from medicalrecordgenerator.data.data_objects import StrokeType, DiagnosisData, OnsetData, AdmissionData, TreatmentData, \
    ImagingData, PostAcuteCareData, PostStrokeComplicationsData, EtiologyData, DischargeData, MedicationData, \
    DiagnosisOcclusionsData, ImagingTreatmentData
from jinja2 import Environment, FileSystemLoader, select_autoescape
from string import Template

from medicalrecordgenerator.data.models import Diagnosis, Onset, Admission, Thrombolysis, Thrombectomy, Treatment, \
    FollowUpImaging, PostAcuteCare, PostStrokeComplications
from medicalrecordgenerator.data.parser import parse_data
from medicalrecordgenerator.generator import generator_helpers


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
    }

    '''
    "etiology": generate_etiology(dictionary.etiology,
                                  data),
    "discharge": generate_discharge(dictionary.discharge,
                                    dictionary.variables.medications,
                                    data)
    '''

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
    thrombolysis = Thrombolysis(treatment_data.dtn, treatment_data.ivt_treatment, treatment_data.ivt_dose)
    thrombectomy = Thrombectomy(treatment_data.dtg, treatment_data.tici_score, treatment_data.dio)

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
    etiology = EtiologyData.from_dict(data)

    etiology_str = ""
    # TODO reasons ??
    reasons = ""

    if etiology.afib_flutter:
        reasons = "afib flutter"

    if etiology.etiology_large_artery:
        pass
    if etiology.etiology_cardioembolism:
        etiology_str = dictionary.cardioembolism.text1
    if etiology.etiology_other:
        pass
    if etiology.etiology_cryptogenic_stroke:
        pass
    if etiology.etiology_small_vessel:
        pass

    substitutes = {
        "reasons": reasons
    }

    return Template(etiology_str).safe_substitute(substitutes)


def generate_discharge(dictionary, variables, data):
    discharge = DischargeData.from_dict(data)
    medication = MedicationData.from_dict(data)

    discharge_str = ""

    discharge_date = discharge.discharge_date.date().strftime('%b %d %Y')
    contact_date = discharge.contact_date.strftime('%b %d %Y at %H:%M') if discharge.contact_date else None
    discharge_medication = generator_helpers.get_medication(variables, medication)

    # TODO findings ?
    findings = []

    if discharge.discharge_destination:
        discharge_str += dictionary.text1
    else:
        discharge_str += dictionary.text2

    if findings:
        discharge_str += dictionary.findings.text1

    if discharge.nihss and discharge.mrs:
        discharge_str += dictionary.scores.text1
    elif discharge.nihss:
        discharge_str += dictionary.scores.text2
    elif discharge.mrs:
        discharge_str += dictionary.scores.text3

    if discharge_medication != "":
        discharge_str += dictionary.medication.text1

    if discharge.contact_date:
        discharge_str += dictionary.next_appointment.text1

    substitutes = {"discharge_date": discharge_date,
                   "discharge_destination": discharge.discharge_destination,
                   "discharge_medication": discharge_medication,
                   "findings": findings,
                   "nihss": discharge.nihss,
                   "mrs": discharge.mrs,
                   "contact_date": contact_date}

    return Template(discharge_str).safe_substitute(substitutes)
