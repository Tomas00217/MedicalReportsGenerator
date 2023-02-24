from datetime import datetime, date
from typing import Optional

DEFAULT_DATE_FORMAT = "%b %d %Y"
DEFAULT_TIME_FORMAT = "%H:%M"


class Diagnosis:
    """
    A class representing diagnosis. Is part of MedicalRecord.

    """

    def __init__(self, stroke_type: Optional[str], aspects_score: Optional[int],
                 imaging_type: Optional[str], occlusion_position: Optional[str]):
        self.stroke_type = stroke_type
        self.aspects_score = aspects_score if aspects_score else None
        self.imaging_type = imaging_type
        self.occlusion_position = occlusion_position


class Patient:
    """
    A class representing patient. Is part of MedicalRecord

    """

    def __init__(self, age: Optional[int], sex: Optional[str], arrival_time: Optional[datetime],
                 arrival_mode: Optional[str], admittance_department: Optional[str], risk_factors: Optional[str],
                 prior_treatment: Optional[str], prenotification: Optional[bool]):
        self.age = age
        self.sex = sex
        self.arrival_time = arrival_time
        self.arrival_mode = arrival_mode
        self.admittance_department = admittance_department
        self.risk_factors = risk_factors
        self.prior_treatment = prior_treatment
        self.prenotification = prenotification


class Onset:
    """
    A class representing onset. Is part of MedicalRecord.

    """

    def __init__(self, onset_timestamp: datetime, wake_up_stroke: Optional[bool],
                 date_format: str, time_format: str):
        self.onset_date = onset_timestamp.date().strftime(date_format if date_format else DEFAULT_DATE_FORMAT)
        self.onset_time = onset_timestamp.time().strftime(time_format if time_format else DEFAULT_TIME_FORMAT)
        self.wake_up_stroke = wake_up_stroke if wake_up_stroke is not None else False


class Admission:
    """
    A class representing admission. Is part of MedicalRecord.

    """

    def __init__(self, admission_nihss: Optional[int], aspects_score: Optional[int], admission_type: Optional[str],
                 sys_blood_pressure: Optional[int], dia_blood_pressure: Optional[int]):
        self.admission_nihss = admission_nihss
        self.aspects_score = aspects_score
        self.admission_type = admission_type
        self.sys_blood_pressure = sys_blood_pressure
        self.dia_blood_pressure = dia_blood_pressure


class Thrombolysis:
    """
    A class representing thrombolysis. Is part of Treatment.

    """

    def __init__(self, dtn: Optional[int], ivt_treatment: Optional[str], ivt_dose: Optional[float]):
        self.dtn = dtn
        self.ivt_treatment = ivt_treatment
        self.ivt_dose = ivt_dose


class Thrombectomy:
    """
    A class representing thrombectomy. Is part of Treatment.

    """

    def __init__(self, dtg: Optional[int], tici_score: Optional[str], dio: Optional[int],
                 tici_score_meaning: Optional[str]):
        self.dtg = dtg
        self.tici_score = tici_score
        self.dio = dio
        self.thrombectomy_transport = dio is not None
        self.tici_score_meaning = tici_score_meaning


class Treatment:
    """
    A class representing treatment. Is part of MedicalRecord.

    """

    def __init__(self, thrombolysis_done: Optional[bool], thrombectomy_done: Optional[bool],
                 thrombolysis_reasons: Optional[str], thrombectomy_reasons: Optional[str],
                 thrombolysis: Thrombolysis, thrombectomy: Thrombectomy):
        self.thrombolysis_done = thrombolysis_done
        self.thrombectomy_done = thrombectomy_done
        self.thrombolysis_reasons = thrombolysis_reasons
        self.thrombectomy_reasons = thrombectomy_reasons
        self.thrombolysis = thrombolysis
        self.thrombectomy = thrombectomy


# class FollowUpImaging:
#     """
#     A class representing follow-up imaging. Is part of MedicalRecord.
#
#     """
#
#     def __init__(self, findings: Optional[str], imaging_type: Optional[str]):
#         self.findings = findings
#         self.imaging_type = imaging_type


class PostAcuteCare:
    """
    A class representing post acute care. Is part of MedicalRecord.

    """

    def __init__(self, afib_flutter: Optional[str], findings: Optional[str], imaging_type: Optional[str],
                 swallowing_screening: Optional[str], physiotherapy_received: Optional[str],
                 ergotherapy_received: Optional[str], speechtherapy_received: Optional[str], therapies: Optional[str]):
        self.afib_flutter = afib_flutter
        self.findings = findings
        self.imaging_type = imaging_type
        self.swallowing_screening = swallowing_screening
        self.physiotherapy = physiotherapy_received is not None and physiotherapy_received == "yes"
        self.ergotherapy = ergotherapy_received is not None and ergotherapy_received == "yes"
        self.speechtherapy = speechtherapy_received is not None and speechtherapy_received == "yes"
        self.therapies = therapies


class PostStrokeComplications:
    """
    A class representing post stroke complications. Is part of MedicalRecord.

    """

    def __init__(self, complications: Optional[str]):
        self.complications = complications if complications != "" else None


class LargeArteryAtherosclerosis:
    """
    A class representing large artery atherosclerosis. Is part of Etiology.

    """

    def __init__(self, carotid_stenosis: Optional[bool], carotid_stenosis_level: Optional[str],
                 carotid_stenosis_followup: Optional[str]):
        self.carotid_stenosis = carotid_stenosis
        self.carotid_stenosis_level = carotid_stenosis_level
        self.carotid_stenosis_followup = carotid_stenosis_followup


class Cardioembolism:
    """
    A class representing cardioembolism. Is part of Etiology.

    """

    def __init__(self, afib_flutter: Optional[str], reasons: Optional[str]):
        self.afib_flutter = afib_flutter
        self.reasons = reasons


class Etiology:
    """
    A class representing etiology. Is part of MedicalRecord.

    """

    def __init__(self, large_artery: Optional[bool], cardioembolism: Optional[bool], other: Optional[bool],
                 cryptogenic_stroke: Optional[bool], small_vessel: Optional[bool],
                 large_artery_atherosclerosis_dat: LargeArteryAtherosclerosis, cardioembolism_dat: Cardioembolism):
        self.large_artery = large_artery
        self.cardioembolism = cardioembolism
        self.other = other
        self.cryptogenic_stroke = cryptogenic_stroke
        self.small_vessel = small_vessel
        self.large_artery_atherosclerosis_dat = large_artery_atherosclerosis_dat
        self.cardioembolism_dat = cardioembolism_dat


class Discharge:
    """
    A class representing discharge. Is part of MedicalRecord.

    """

    def __init__(self, discharge_date: date, discharge_destination: Optional[str], nihss: Optional[int],
                 mrs: Optional[int], contact_date: Optional[datetime], mode_contact: Optional[str],
                 discharge_medication: str, date_format: str):
        self.discharge_date = discharge_date.strftime(date_format if date_format else DEFAULT_DATE_FORMAT)
        self.discharge_destination = discharge_destination
        self.nihss = nihss
        self.mrs = mrs,
        self.contact_date = contact_date.strftime(date_format if date_format else DEFAULT_DATE_FORMAT) \
            if contact_date else None
        self.mode_contact = mode_contact
        self.discharge_medication = discharge_medication


class MedicalRecord:
    """
    A class representing the final Medical record composed of smaller parts.

    """

    def __init__(self, diagnosis: Diagnosis, patient: Patient, onset: Onset, admission: Admission, treatment: Treatment,
                 post_acute_care: Optional[PostAcuteCare], post_stroke_complications: PostStrokeComplications,
                 etiology: Optional[Etiology], discharge: Discharge):
        self.diagnosis = diagnosis
        self.patient = patient
        self.onset = onset
        self.admission = admission
        self.treatment = treatment
        # self.follow_up_imaging = follow_up_imaging
        self.post_acute_care = post_acute_care
        self.post_stroke_complications = post_stroke_complications
        self.etiology = etiology
        self.discharge = discharge

    def to_dict(self):
        """Creates a dictionary from the attributes

        Returns
        -------
        dict
            Dictionary of all attributes from child classes
        """
        data = {
            "diagnosis": vars(self.diagnosis) if self.diagnosis else {},
            "patient": vars(self.patient) if self.patient else {},
            "onset": vars(self.onset) if self.onset else {},
            "admission": vars(self.admission) if self.admission else {},
            "treatment": vars(self.treatment) if self.treatment else {},
            # "follow_up_imaging": vars(self.follow_up_imaging) if self.follow_up_imaging else {},
            "post_acute_care": vars(self.post_acute_care) if self.post_acute_care else {},
            "post_stroke_complications": vars(self.post_stroke_complications) if self.post_stroke_complications else {},
            "etiology": vars(self.etiology) if self.etiology else {},
            "discharge": vars(self.discharge) if self.discharge else {},
        }

        if self.treatment:
            data["treatment"].update(vars(self.treatment.thrombolysis))
            data["treatment"].update(vars(self.treatment.thrombectomy))
        if self.etiology:
            data["etiology"].update(vars(self.etiology.large_artery_atherosclerosis_dat))
            data["etiology"].update(vars(self.etiology.cardioembolism_dat))

        return data
