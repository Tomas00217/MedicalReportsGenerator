def get_occlusion(occlusions, diagnosis):
    occlusions_str = ""

    if diagnosis.occlusion_left_mca_m1:
        occlusions_str += occlusions['left_mca_m1']
    if diagnosis.occlusion_left_mca_m2:
        occlusions_str += occlusions['left_mca_m2'] if occlusions_str == "" else f", {occlusions['left_mca_m2']}"
    if diagnosis.occlusion_left_mca_m2:
        occlusions_str += occlusions['left_mca_m3'] if occlusions_str == "" else f", {occlusions['left_mca_m3']}"
    if diagnosis.occlusion_left_aca:
        occlusions_str += occlusions['left_aca'] if occlusions_str == "" else f", {occlusions['left_aca']}"
    if diagnosis.occlusion_left_pca_p1:
        occlusions_str += occlusions['left_pca_p1'] if occlusions_str == "" else f", {occlusions['left_pca_p1']}"
    if diagnosis.occlusion_left_pca_p2:
        occlusions_str += occlusions['left_pca_p2'] if occlusions_str == "" else f", {occlusions['left_pca_p2']}"
    if diagnosis.occlusion_left_cae:
        occlusions_str += occlusions['left_cae'] if occlusions_str == "" else f", {occlusions['left_cae']}"
    if diagnosis.occlusion_left_cai:
        occlusions_str += occlusions['left_cai'] if occlusions_str == "" else f", {occlusions['left_cai']}"
    if diagnosis.occlusion_right_mca_m1:
        occlusions_str += occlusions['right_mca_m1'] if occlusions_str == "" else f", {occlusions['right_mca_m1']}"
    if diagnosis.occlusion_right_mca_m2:
        occlusions_str += occlusions['right_mca_m2'] if occlusions_str == "" else f", {occlusions['right_mca_m2']}"
    if diagnosis.occlusion_right_mca_m3:
        occlusions_str += occlusions['right_mca_m3'] if occlusions_str == "" else f", {occlusions['right_mca_m3']}"
    if diagnosis.occlusion_right_aca:
        occlusions_str += occlusions['right_aca'] if occlusions_str == "" else f", {occlusions['right_aca']}"
    if diagnosis.occlusion_right_pca_p1:
        occlusions_str += occlusions['right_pca_p1'] if occlusions_str == "" else f", {occlusions['right_pca_p1']}"
    if diagnosis.occlusion_right_pca_p2:
        occlusions_str += occlusions['right_pca_p2'] if occlusions_str == "" else f", {occlusions['right_pca_p2']}"
    if diagnosis.occlusion_right_cae:
        occlusions_str += occlusions['right_cae'] if occlusions_str == "" else f", {occlusions['right_cae']}"
    if diagnosis.occlusion_right_cai:
        occlusions_str += occlusions['right_cai'] if occlusions_str == "" else f", {occlusions['right_cai']}"
    if diagnosis.occlusion_ba:
        occlusions_str += occlusions['ba'] if occlusions_str == "" else f", {occlusions['ba']}"
    if diagnosis.occlusion_va:
        occlusions_str += occlusions['va'] if occlusions_str == "" else f", {occlusions['va']}"

    return occlusions_str


def get_imaging_findings(findings, imaging):
    findings_str = ""

    if imaging.post_treatment_infarction:
        findings_str += findings['infarction']
    if imaging.post_treatment_no_bleeding:
        findings_str += findings['no_bleeding'] if findings_str == "" else f", {['findings.no_bleeding']}"
    if imaging.post_treatment_remote:
        findings_str += findings['remote'] if findings_str == "" else f", {['findings.remote']}"
    if imaging.post_treatment_hi_i:
        findings_str += findings['hi_i'] if findings_str == "" else f", {['findings.hi_i']}"
    if imaging.post_treatment_hi_ii:
        findings_str += findings['hi_ii'] if findings_str == "" else f", {['findings.hi_ii']}"
    if imaging.post_treatment_ph_i:
        findings_str += findings['ph_i'] if findings_str == "" else f", {['findings.ph_i']}"
    if imaging.post_treatment_ph_ii:
        findings_str += findings['ph_ii'] if findings_str == "" else f", {['findings.ph_ii']}"

    return findings_str


def get_therapies(therapies, post_acute_care):
    therapies_str = ""

    if post_acute_care.physiotherapy:
        therapies_str += therapies['physiotherapy']
    if post_acute_care.ergotherapy:
        therapies_str += therapies['ergotherapy'] if therapies_str == "" else f", {therapies['ergotherapy']}"
    if post_acute_care.speechtherapy:
        therapies_str += therapies['speechtherapy'] if therapies_str == "" else f", {therapies['speechtherapy']}"

    return therapies_str


def get_complications(complications, post_stroke):
    complications_str = ""

    if post_stroke.post_stroke_pneumonia:
        complications_str += complications.pneumonia
    if post_stroke.post_stroke_dvt:
        complications_str += complications.dvt if complications_str == "" else f", {complications.dvt}"
    if post_stroke.post_stroke_embolism:
        complications_str += complications.embolism if complications_str == "" else f", {complications.embolism}"
    if post_stroke.post_stroke_infection:
        complications_str += complications.infection if complications_str == "" else f", {complications.infection}"
    if post_stroke.post_stroke_sores:
        complications_str += complications.sores if complications_str == "" else f", {complications.sores}"
    if post_stroke.post_stroke_sepsis:
        complications_str += complications.sepsis if complications_str == "" else f", {complications.sepsis}"
    if post_stroke.post_stroke_extension:
        complications_str += complications.extension if complications_str == "" else f", {complications.extension}"
    if post_stroke.post_stroke_other:
        complications_str += complications.other if complications_str == "" else f", {complications.other}"
    if post_stroke.post_stroke_none:
        complications_str += complications.none if complications_str == "" else f", {complications.none}"

    return complications_str


def get_medication(medications, meds):
    medications_str = ""

    if meds.discharge_antidiabetics:
        medications_str += medications.antidiabetics
    if meds.discharge_antihypertensives:
        medications_str += medications.antihypertensives \
            if medications_str == "" else f", {medications.antihypertensives}"
    if meds.discharge_asa:
        medications_str += medications.asa if medications_str == "" else f", {medications.asa}"
    if meds.discharge_cilostazol:
        medications_str += medications.cilostazol if medications_str == "" else f", {medications.cilostazol}"
    if meds.discharge_clopidrogel:
        medications_str += medications.clopidrogel if medications_str == "" else f", {medications.clopidrogel}"
    if meds.discharge_ticagrelor:
        medications_str += medications.ticagrelor if medications_str == "" else f", {medications.ticagrelor}"
    if meds.discharge_ticlopidine:
        medications_str += medications.ticlopidine if medications_str == "" else f", {medications.ticlopidine}"
    if meds.discharge_prasugrel:
        medications_str += medications.prasugrel if medications_str == "" else f", {medications.prasugrel}"
    if meds.discharge_dipyridamol:
        medications_str += medications.dipyridamol if medications_str == "" else f", {medications.dipyridamol}"
    if meds.discharge_warfarin:
        medications_str += medications.warfarin if medications_str == "" else f", {medications.warfarin}"
    if meds.discharge_dabigatran:
        medications_str += medications.dabigatran if medications_str == "" else f", {medications.dabigatran}"
    if meds.discharge_rivaroxaban:
        medications_str += medications.rivaroxaban if medications_str == "" else f", {medications.rivaroxaban}"
    if meds.discharge_apixaban:
        medications_str += medications.apixaban if medications_str == "" else f", {medications.apixaban}"
    if meds.discharge_edoxaban:
        medications_str += medications.edoxaban if medications_str == "" else f", {medications.edoxaban}"
    if meds.discharge_statin:
        medications_str += medications.statin if medications_str == "" else f", {medications.statin}"
    if meds.discharge_heparin:
        medications_str += medications.heparin if medications_str == "" else f", {medications.heparin}"
    if meds.discharge_other:
        medications_str += medications.other if medications_str == "" else f", {medications.other}"
    if meds.discharge_anticoagulant_recommended:
        medications_str += medications.anticoagulant_recommended \
            if medications_str == "" else f", {medications.anticoagulant_recommended}"

    """
    if meds.discharge_other_antiplatelet:
        medications_str += medications.other_antiplatelet 
            if medications_str == "" else f", {medications.other_antiplatelet}"
    if meds.discharge_other_anticoagulant:
        medications_str += medications.other_anticoagulant 
            if medications_str == "" else f", {medications.other_anticoagulant}"
    if meds.discharge_any_anticoagulant:
        medications_str += medications.any_anticoagulant 
            if medications_str == "" else f", {medications.any_anticoagulant}"
    if meds.discharge_any_antiplatelet:
        medications_str += medications.any_antiplatelet 
            if medications_str == "" else f", {medications.any_antiplatelet}"
    """

    return medications_str
