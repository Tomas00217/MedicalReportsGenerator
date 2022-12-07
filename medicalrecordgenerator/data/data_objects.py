from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import Optional

from dict_to_dataclass import DataclassFromDict, field_from_dict


class StrokeType(Enum):
    Ischemic = "ischemic"
    IntracerebralHemorrhage = "intracerebral hemorrhage"
    TransientIschemic = "transient ischemic"
    SubarachnoidHemorrhage = "subarachnoid hemorrhage"
    CerebralVenousThrombosis = "cerebral venous thrombosis"
    StrokeMimics = "stroke mimics"
    Undetermined = "undetermined"


@dataclass()
class DiagnosisData(DataclassFromDict):
    stroke_type: Optional[str] = field_from_dict(default=None)
    aspects_score: Optional[float] = field_from_dict(default=None)
    imaging_type: Optional[str] = field_from_dict(default=None)


@dataclass()
class DiagnosisOcclusionsData(DataclassFromDict):
    occlusion_left_mca_m1: Optional[bool] = field_from_dict(default=None)
    occlusion_left_mca_m2: Optional[bool] = field_from_dict(default=None)
    occlusion_left_mca_m3: Optional[bool] = field_from_dict(default=None)
    occlusion_left_aca: Optional[bool] = field_from_dict(default=None)
    occlusion_left_pca_p1: Optional[bool] = field_from_dict(default=None)
    occlusion_left_pca_p2: Optional[bool] = field_from_dict(default=None)
    occlusion_left_cae: Optional[bool] = field_from_dict(default=None)
    occlusion_left_cai: Optional[bool] = field_from_dict(default=None)
    occlusion_right_mca_m1: Optional[bool] = field_from_dict(default=None)
    occlusion_right_mca_m2: Optional[bool] = field_from_dict(default=None)
    occlusion_right_mca_m3: Optional[bool] = field_from_dict(default=None)
    occlusion_right_aca: Optional[bool] = field_from_dict(default=None)
    occlusion_right_pca_p1: Optional[bool] = field_from_dict(default=None)
    occlusion_right_pca_p2: Optional[bool] = field_from_dict(default=None)
    occlusion_right_cae: Optional[bool] = field_from_dict(default=None)
    occlusion_right_cai: Optional[bool] = field_from_dict(default=None)
    occlusion_ba: Optional[bool] = field_from_dict(default=None)
    occlusion_va: Optional[bool] = field_from_dict(default=None)


@dataclass()
class OnsetData(DataclassFromDict):
    onset_timestamp: datetime = field_from_dict()
    wake_up_stroke: Optional[bool] = field_from_dict(default=None)


@dataclass()
class AdmissionData(DataclassFromDict):
    hospitalized_in: Optional[str] = field_from_dict(default=None)
    nihss_score: Optional[float] = field_from_dict(default=None)


@dataclass()
class TreatmentData(DataclassFromDict):
    thrombolysis: Optional[bool] = field_from_dict(default=None)
    dtn: Optional[float] = field_from_dict("door_to_needle", default=None)
    ivt_treatment: Optional[str] = field_from_dict(default=None)
    ivt_dose: Optional[float] = field_from_dict(default=None)
    no_thrombolysis_reason: Optional[str] = field_from_dict(default=None)
    thrombectomy: Optional[bool] = field_from_dict(default=None)
    dtg: Optional[float] = field_from_dict("door_to_groin", default=None)
    tici_score: Optional[float] = field_from_dict(default=None)
    no_thrombectomy_reason: Optional[str] = field_from_dict(default=None)
    dio: Optional[float] = field_from_dict("door_to_door", default=None)
    thrombectomy_transport: bool = False


@dataclass()
class ImagingData(DataclassFromDict):
    imaging_type: Optional[str] = field_from_dict("post_treatment_imaging", default=None)
    aspects_score: Optional[float] = field_from_dict(default=None)


@dataclass()
class ImagingTreatmentData(DataclassFromDict):
    post_treatment_infarction: Optional[bool] = field_from_dict(default=None)
    post_treatment_no_bleeding: Optional[bool] = field_from_dict(default=None)
    post_treatment_remote: Optional[bool] = field_from_dict(default=None)
    post_treatment_hi_i: Optional[bool] = field_from_dict(default=None)
    post_treatment_hi_ii: Optional[bool] = field_from_dict(default=None)
    post_treatment_ph_i: Optional[bool] = field_from_dict(default=None)
    post_treatment_ph_ii: Optional[bool] = field_from_dict(default=None)


@dataclass()
class PostAcuteCareData(DataclassFromDict):
    dysphagia_screening: Optional[str] = field_from_dict("dysphagia_screening_done", default=None)
    physiotherapy_received: Optional[str] = field_from_dict(default=None)
    occup_physiotherapy_received: Optional[str] = field_from_dict(default=None)
    speech_therapy_received: Optional[str] = field_from_dict(default=None)


@dataclass()
class PostStrokeComplicationsData(DataclassFromDict):
    post_stroke_pneumonia: Optional[bool] = field_from_dict(default=None)
    post_stroke_dvt: Optional[bool] = field_from_dict(default=None)
    post_stroke_embolism: Optional[bool] = field_from_dict(default=None)
    post_stroke_infection: Optional[bool] = field_from_dict(default=None)
    post_stroke_sores: Optional[bool] = field_from_dict(default=None)
    post_stroke_sepsis: Optional[bool] = field_from_dict(default=None)
    post_stroke_extension: Optional[bool] = field_from_dict(default=None)
    post_stroke_other: Optional[bool] = field_from_dict(default=None)
    post_stroke_none: Optional[bool] = field_from_dict(default=None)


@dataclass()
class EtiologyData(DataclassFromDict):
    etiology_large_artery: Optional[bool] = field_from_dict(default=None)
    etiology_cardioembolism: Optional[bool] = field_from_dict(default=None)
    etiology_other: Optional[bool] = field_from_dict(default=None)
    etiology_cryptogenic_stroke: Optional[bool] = field_from_dict(default=None)
    etiology_small_vessel: Optional[bool] = field_from_dict(default=None)
    carotid_stenosis: Optional[bool] = field_from_dict(default=None)
    carotid_stenosis_level: Optional[str] = field_from_dict(default=None)
    carotid_stenosis_followup: Optional[str] = field_from_dict(default=None)
    afib_flutter: Optional[str] = field_from_dict(default=None)


@dataclass()
class DischargeData(DataclassFromDict):
    discharge_date: datetime = field_from_dict()
    discharge_destination: Optional[str] = field_from_dict(default=None)
    nihss: Optional[float] = field_from_dict("discharge_nihss_score", default=None)
    mrs: Optional[float] = field_from_dict("discharge_mrs", default=None)
    contact_date: Optional[datetime] = field_from_dict(default=None)
    mode_contact: Optional[str] = field_from_dict(default=None)


@dataclass()
class MedicationData(DataclassFromDict):
    discharge_antidiabetics: Optional[bool] = field_from_dict(default=None)
    discharge_antihypertensives: Optional[bool] = field_from_dict(default=None)
    discharge_asa: Optional[bool] = field_from_dict(default=None)
    discharge_cilostazol: Optional[bool] = field_from_dict(default=None)
    discharge_clopidrogel: Optional[bool] = field_from_dict(default=None)
    discharge_ticagrelor: Optional[bool] = field_from_dict(default=None)
    discharge_ticlopidine: Optional[bool] = field_from_dict(default=None)
    discharge_prasugrel: Optional[bool] = field_from_dict(default=None)
    discharge_dipyridamol: Optional[bool] = field_from_dict(default=None)
    discharge_warfarin: Optional[bool] = field_from_dict(default=None)
    discharge_dabigatran: Optional[bool] = field_from_dict(default=None)
    discharge_rivaroxaban: Optional[bool] = field_from_dict(default=None)
    discharge_apixaban: Optional[bool] = field_from_dict(default=None)
    discharge_edoxaban: Optional[bool] = field_from_dict(default=None)
    discharge_statin: Optional[bool] = field_from_dict(default=None)
    discharge_heparin: Optional[bool] = field_from_dict(default=None)
    discharge_other: Optional[bool] = field_from_dict(default=None)
    discharge_anticoagulant_recommended: Optional[bool] = field_from_dict(default=None)
    discharge_other_antiplatelet: Optional[bool] = field_from_dict(default=None)
    discharge_other_anticoagulant: Optional[bool] = field_from_dict(default=None)
    discharge_any_anticoagulant: Optional[bool] = field_from_dict(default=None)
    discharge_any_antiplatelet: Optional[bool] = field_from_dict(default=None)
