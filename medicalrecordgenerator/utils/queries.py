def select_all(ordered: bool) -> str:
    pfx = "strokehealthcaremodel"

    query = f"""
        SELECT SHCM.*, STM.name AS stroke_type, ITM.name AS imaging_type, SM.name AS sex, 
        ADM.name AS admittance_department, AMM.name AS arrival_mode, HIM.name AS hospitalized_in, 
        IVTTM.name AS ivt_treatment, NTTR.name as no_thrombectomy_reason, NTLR.name AS no_thrombolysis_reason,
        PTIM.name AS post_treatment_imaging, TSM.name AS tici_score, SSDM.name AS swallowing_screening_done,
        SSTM.name AS swallowing_screening_type, PTDM.name AS physiotherapy_received, 
        OTDM.name AS occup_physiotherapy_received, STDM.name AS speech_therapy_received, AFM.name AS afib_flutter, 
        DDM.name AS discharge_destination, MDM.name AS mode_contact, CSLM.name AS carotid_stenosis_level, 
        DTM.name as department_type
        
        FROM {pfx}_strokehealthcaremodel AS SHCM
        
        LEFT JOIN {pfx}_stroketypemodel AS STM
        ON SHCM.stroke_type_id = STM.id
        
        LEFT JOIN {pfx}_imagingtypemodel AS ITM
        ON SHCM.imaging_type_id = ITM.id
        
        LEFT JOIN {pfx}_sexmodel AS SM
        ON SHCM.sex_id = SM.id
        
        LEFT JOIN {pfx}_admittancedepartmentmodel AS ADM
        ON SHCM.admittance_department_id = ADM.id
        
        LEFT JOIN {pfx}_arrivalmodemodel AS AMM
        ON SHCM.arrival_mode_id = AMM.id
        
        LEFT JOIN {pfx}_hospitalizedinmodel AS HIM
        ON SHCM.hospitalized_in_id = HIM.id
        
        LEFT JOIN {pfx}_ivttreatmentmodel AS IVTTM
        ON SHCM.ivt_treatment_id = IVTTM.id
        
        LEFT JOIN {pfx}_nothrombectomyreasonmodel AS NTTR
        ON SHCM.no_thrombectomy_reason_id = NTTR.id
        
        LEFT JOIN {pfx}_nothrombolysisreasonmodel AS NTLR
        ON SHCM.no_thrombolysis_reason_id = NTLR.id
        
        LEFT JOIN {pfx}_posttreatmentimagingmodel as PTIM
        ON SHCM.post_treatment_imaging_id = PTIM.id
        
        LEFT JOIN {pfx}_mticiscoremodel AS TSM
        ON SHCM.mtici_score_id = TSM.id
        
        LEFT JOIN {pfx}_swallowingscreeningdonemodel AS SSDM
        ON SHCM.swallowing_screening_done_id = SSDM.id
        
        LEFT JOIN {pfx}_swallowingscreeningtypemodel AS SSTM
        ON SHCM.swallowing_screening_type_id = SSTM.id
                
        LEFT JOIN {pfx}_physiotherapydonemodel AS PTDM
        ON SHCM.physiotherapy_done_id = PTDM.id
                
        LEFT JOIN {pfx}_occupationaltherapydonemodel AS OTDM
        ON SHCM.occup_physiotherapy_done_id = OTDM.id
        
        LEFT JOIN {pfx}_speechtherapydonemodel AS STDM
        ON SHCM.speech_therapy_done_id = STDM.id
        
        LEFT JOIN {pfx}_afibfluttermodel AS AFM
        ON SHCM.afib_flutter_id = AFM.id
        
        LEFT JOIN {pfx}_dischargedestinationmodel AS DDM
        ON SHCM.discharge_destination_id = DDM.id
        
        LEFT JOIN {pfx}_modecontactmodel AS MDM
        ON SHCM.mode_contact_id = MDM.id
                
        LEFT JOIN {pfx}_carotidstenosislevelmodel AS CSLM
        ON SHCM.carotid_stenosis_level_id = CSLM.id
        
        LEFT JOIN {pfx}_departmenttypemodel AS DTM
        ON SHCM.department_type_id = DTM.id
    """

    if ordered:
        query += "ORDER BY SHCM.subject_id"

    return query


def select_by_id(subject_id: int) -> str:
    query = select_all(False)

    query += f" WHERE SHCM.subject_id={subject_id}"

    return query


def select_subject_ids() -> str:
    query = "SELECT subject_id FROM strokehealthcaremodel_strokehealthcaremodel ORDER BY subject_id"

    return query
