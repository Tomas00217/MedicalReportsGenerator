from datetime import time
from string import Template
from typing import Optional, Any

from medicalrecordgenerator.data.parser import parse


class GeneratedObject:
    def generate(self, dictionary):
        text = self.get_text(dictionary)

        return Template(text).safe_substitute(vars(self))

    def get_text(self, dictionary):
        text = parse(dictionary, vars(self))

        return text if text else ""


class Diagnosis(GeneratedObject):
    def __init__(self, stroke_type: Optional[str], aspects_score: Optional[int],
                 imaging_type: Optional[str], occlusion_position: Optional[str]):
        self.stroke_type = stroke_type
        self.aspects_score = int(aspects_score) if aspects_score else None
        self.imaging_type = imaging_type
        self.occlusion_position = occlusion_position


class Onset(GeneratedObject):
    def __init__(self, onset_date: str, onset_time: Optional[time], wake_up_stroke: Optional[bool]):
        self.onset_date = onset_date
        self.onset_time = onset_time
        self.wake_up_stroke = wake_up_stroke if wake_up_stroke is not None else False


class Admission(GeneratedObject):
    def __init__(self, admission_nihss: Optional[int], admission_type: Optional[str]):
        self.admission_nihss = int(admission_nihss) if admission_nihss else None
        self.admission_type = admission_type


class Thrombolysis(GeneratedObject):
    def __init__(self, dtn: Optional[int], ivt_treatment: Optional[str], ivt_dose: Optional[float]):
        self.dtn = int(dtn) if dtn else None
        self.ivt_treatment = ivt_treatment
        self.ivt_dose = ivt_dose


class Thrombectomy(GeneratedObject):
    def __init__(self, dtg: Optional[int], tici_score: Optional[str], dio: Optional[int]):
        self.dtg = int(dtg) if dtg else None
        self.tici_score = tici_score
        self.dio = int(dio) if dio else None
        self.thrombectomy_transport = dio is not None
        self.tici_score_meaning = "TODO"


class Treatment(GeneratedObject):
    def __init__(self, thrombolysis_done: Optional[bool], thrombectomy_done: Optional[bool],
                 thrombolysis_reasons: Optional[str], thrombectomy_reasons: Optional[str],
                 thrombolysis: Thrombolysis, thrombectomy: Thrombectomy):
        self.thrombolysis_done = thrombolysis_done
        self.thrombectomy_done = thrombectomy_done
        self.thrombolysis_reasons = thrombolysis_reasons
        self.thrombectomy_reasons = thrombectomy_reasons
        self.thrombolysis = thrombolysis
        self.thrombectomy = thrombectomy

    def get_text(self, dictionary):
        dict_to_parse = vars(self)
        dict_to_parse.update(vars(self.thrombolysis))
        dict_to_parse.update(vars(self.thrombectomy))

        text = parse(dictionary, vars(self))

        return text if text else ""


class FollowUpImaging(GeneratedObject):
    def __init__(self, findings: Optional[str], imaging_type: Optional[str], aspects_score: Optional[int]):
        self.findings = findings
        self.imaging_type = imaging_type
        self.aspects_score = int(aspects_score) if aspects_score else None


class PostAcuteCare(GeneratedObject):
    def __init__(self, dysphagia_screening: Optional[str], physiotherapy_received: Optional[str],
                 ergotherapy_received: Optional[str], speechtherapy_received: Optional[str], therapies: Optional[str]):
        self.dysphagia_screening = dysphagia_screening
        self.physiotherapy = physiotherapy_received is not None and physiotherapy_received == "yes"
        self.ergotherapy = ergotherapy_received is not None and ergotherapy_received == "yes"
        self.speechtherapy = speechtherapy_received is not None and speechtherapy_received == "yes"
        self.therapies = therapies


class PostStrokeComplications(GeneratedObject):
    def __init__(self, complications: Optional[str]):
        self.complications = complications if complications != "" else None


class Etiology(GeneratedObject):
    def __init__(self):
        pass


class Discharge(GeneratedObject):
    def __init__(self):
        pass
