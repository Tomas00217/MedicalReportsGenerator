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
