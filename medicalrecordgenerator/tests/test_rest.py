import unittest
import io
import re
from unittest import mock

from app.app_operations import generate
from utils.db_operations import get_patient_info_from_db
from utils.queries import select_all, select_by_id


class TestGenerate(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def assert_stdout_for_generate(self, subject_id, expected_output, mock_stdout):
        generate("en_US", False, subject_id)
        self.assertEqual(expected_output.strip(), mock_stdout.getvalue().strip())

    def test_generate_all(self):
        with open('fixtures/expected_result.txt') as f:
            expected = f.read()

        self.assert_stdout_for_generate(None, expected)

    def test_generate_by_id(self):
        with open('fixtures/expected_result.txt') as f:
            expected = f.readlines()

        for i in range(1, 8):
            with self.subTest(f"Test subject with id {i}"):
                self.assert_stdout_for_generate(i, expected[i-1])


class TestDbOperations(unittest.TestCase):
    @staticmethod
    def fix_dbc():
        dbc = mock.MagicMock(spec=['cursor'])
        dbc.autocommit = True

        return dbc

    def test_get_patient_info_from_db(self):
        dbc = self.fix_dbc()

        get_patient_info_from_db(dbc)

        with dbc.cursor() as cursor:
            expect_sql = select_all(True)
            calls = [mock.call.execute(expect_sql), mock.call.fetchall()]
            cursor.assert_has_calls(calls)
        self.assertTrue(dbc.autocommit)

    def test_select_all(self):
        result = re.sub(r"\s+", "", select_all(True), flags=re.UNICODE)
        expected = re.sub(r"\s+", "", '''
        SELECT SHCM.*, STM.name AS stroke_type, ITM.name AS imaging_type, SM.name AS sex, 
        ADM.name AS admittance_department, AMM.name AS arrival_mode, HIM.name AS hospitalized_in, 
        IVTTM.name AS ivt_treatment, NTTR.name as no_thrombectomy_reason, NTLR.name AS no_thrombolysis_reason,
        PTIM.name AS post_treatment_imaging, TSM.name AS tici_score, SSDM.name AS swallowing_screening_done,
        SSTM.name AS swallowing_screening_type, PTDM.name AS physiotherapy_received, 
        OTDM.name AS occup_physiotherapy_received, STDM.name AS speech_therapy_received, AFM.name AS afib_flutter, 
        DDM.name AS discharge_destination, MDM.name AS mode_contact, CSLM.name AS carotid_stenosis_level, 
        DTM.name as department_type

        FROM strokehealthcaremodel_strokehealthcaremodel AS SHCM

        LEFT JOIN strokehealthcaremodel_stroketypemodel AS STM
        ON SHCM.stroke_type_id = STM.id

        LEFT JOIN strokehealthcaremodel_imagingtypemodel AS ITM
        ON SHCM.imaging_type_id = ITM.id

        LEFT JOIN strokehealthcaremodel_sexmodel AS SM
        ON SHCM.sex_id = SM.id

        LEFT JOIN strokehealthcaremodel_admittancedepartmentmodel AS ADM
        ON SHCM.admittance_department_id = ADM.id

        LEFT JOIN strokehealthcaremodel_arrivalmodemodel AS AMM
        ON SHCM.arrival_mode_id = AMM.id

        LEFT JOIN strokehealthcaremodel_hospitalizedinmodel AS HIM
        ON SHCM.hospitalized_in_id = HIM.id

        LEFT JOIN strokehealthcaremodel_ivttreatmentmodel AS IVTTM
        ON SHCM.ivt_treatment_id = IVTTM.id

        LEFT JOIN strokehealthcaremodel_nothrombectomyreasonmodel AS NTTR
        ON SHCM.no_thrombectomy_reason_id = NTTR.id

        LEFT JOIN strokehealthcaremodel_nothrombolysisreasonmodel AS NTLR
        ON SHCM.no_thrombolysis_reason_id = NTLR.id

        LEFT JOIN strokehealthcaremodel_posttreatmentimagingmodel as PTIM
        ON SHCM.post_treatment_imaging_id = PTIM.id

        LEFT JOIN strokehealthcaremodel_mticiscoremodel AS TSM
        ON SHCM.mtici_score_id = TSM.id

        LEFT JOIN strokehealthcaremodel_swallowingscreeningdonemodel AS SSDM
        ON SHCM.swallowing_screening_done_id = SSDM.id

        LEFT JOIN strokehealthcaremodel_swallowingscreeningtypemodel AS SSTM
        ON SHCM.swallowing_screening_type_id = SSTM.id

        LEFT JOIN strokehealthcaremodel_physiotherapydonemodel AS PTDM
        ON SHCM.physiotherapy_done_id = PTDM.id

        LEFT JOIN strokehealthcaremodel_occupationaltherapydonemodel AS OTDM
        ON SHCM.occup_physiotherapy_done_id = OTDM.id

        LEFT JOIN strokehealthcaremodel_speechtherapydonemodel AS STDM
        ON SHCM.speech_therapy_done_id = STDM.id

        LEFT JOIN strokehealthcaremodel_afibfluttermodel AS AFM
        ON SHCM.afib_flutter_id = AFM.id

        LEFT JOIN strokehealthcaremodel_dischargedestinationmodel AS DDM
        ON SHCM.discharge_destination_id = DDM.id

        LEFT JOIN strokehealthcaremodel_modecontactmodel AS MDM
        ON SHCM.mode_contact_id = MDM.id

        LEFT JOIN strokehealthcaremodel_carotidstenosislevelmodel AS CSLM
        ON SHCM.carotid_stenosis_level_id = CSLM.id

        LEFT JOIN strokehealthcaremodel_departmenttypemodel AS DTM
        ON SHCM.department_type_id = DTM.id
        
        ORDER BY SHCM.subject_id
        ''', flags=re.UNICODE)

        self.assertEqual(expected, result)

    def test_select_by_id(self):
        result = re.sub(r"\s+", "", select_by_id(1), flags=re.UNICODE)
        expected = re.sub(r"\s+", "", '''
        SELECT SHCM.*, STM.name AS stroke_type, ITM.name AS imaging_type, SM.name AS sex, 
        ADM.name AS admittance_department, AMM.name AS arrival_mode, HIM.name AS hospitalized_in, 
        IVTTM.name AS ivt_treatment, NTTR.name as no_thrombectomy_reason, NTLR.name AS no_thrombolysis_reason,
        PTIM.name AS post_treatment_imaging, TSM.name AS tici_score, SSDM.name AS swallowing_screening_done,
        SSTM.name AS swallowing_screening_type, PTDM.name AS physiotherapy_received, 
        OTDM.name AS occup_physiotherapy_received, STDM.name AS speech_therapy_received, AFM.name AS afib_flutter, 
        DDM.name AS discharge_destination, MDM.name AS mode_contact, CSLM.name AS carotid_stenosis_level, 
        DTM.name as department_type

        FROM strokehealthcaremodel_strokehealthcaremodel AS SHCM

        LEFT JOIN strokehealthcaremodel_stroketypemodel AS STM
        ON SHCM.stroke_type_id = STM.id

        LEFT JOIN strokehealthcaremodel_imagingtypemodel AS ITM
        ON SHCM.imaging_type_id = ITM.id

        LEFT JOIN strokehealthcaremodel_sexmodel AS SM
        ON SHCM.sex_id = SM.id

        LEFT JOIN strokehealthcaremodel_admittancedepartmentmodel AS ADM
        ON SHCM.admittance_department_id = ADM.id

        LEFT JOIN strokehealthcaremodel_arrivalmodemodel AS AMM
        ON SHCM.arrival_mode_id = AMM.id

        LEFT JOIN strokehealthcaremodel_hospitalizedinmodel AS HIM
        ON SHCM.hospitalized_in_id = HIM.id

        LEFT JOIN strokehealthcaremodel_ivttreatmentmodel AS IVTTM
        ON SHCM.ivt_treatment_id = IVTTM.id

        LEFT JOIN strokehealthcaremodel_nothrombectomyreasonmodel AS NTTR
        ON SHCM.no_thrombectomy_reason_id = NTTR.id

        LEFT JOIN strokehealthcaremodel_nothrombolysisreasonmodel AS NTLR
        ON SHCM.no_thrombolysis_reason_id = NTLR.id

        LEFT JOIN strokehealthcaremodel_posttreatmentimagingmodel as PTIM
        ON SHCM.post_treatment_imaging_id = PTIM.id

        LEFT JOIN strokehealthcaremodel_mticiscoremodel AS TSM
        ON SHCM.mtici_score_id = TSM.id

        LEFT JOIN strokehealthcaremodel_swallowingscreeningdonemodel AS SSDM
        ON SHCM.swallowing_screening_done_id = SSDM.id

        LEFT JOIN strokehealthcaremodel_swallowingscreeningtypemodel AS SSTM
        ON SHCM.swallowing_screening_type_id = SSTM.id

        LEFT JOIN strokehealthcaremodel_physiotherapydonemodel AS PTDM
        ON SHCM.physiotherapy_done_id = PTDM.id

        LEFT JOIN strokehealthcaremodel_occupationaltherapydonemodel AS OTDM
        ON SHCM.occup_physiotherapy_done_id = OTDM.id

        LEFT JOIN strokehealthcaremodel_speechtherapydonemodel AS STDM
        ON SHCM.speech_therapy_done_id = STDM.id

        LEFT JOIN strokehealthcaremodel_afibfluttermodel AS AFM
        ON SHCM.afib_flutter_id = AFM.id

        LEFT JOIN strokehealthcaremodel_dischargedestinationmodel AS DDM
        ON SHCM.discharge_destination_id = DDM.id

        LEFT JOIN strokehealthcaremodel_modecontactmodel AS MDM
        ON SHCM.mode_contact_id = MDM.id

        LEFT JOIN strokehealthcaremodel_carotidstenosislevelmodel AS CSLM
        ON SHCM.carotid_stenosis_level_id = CSLM.id

        LEFT JOIN strokehealthcaremodel_departmenttypemodel AS DTM
        ON SHCM.department_type_id = DTM.id WHERE SHCM.subject_id=1
        ''', flags=re.UNICODE)

        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
