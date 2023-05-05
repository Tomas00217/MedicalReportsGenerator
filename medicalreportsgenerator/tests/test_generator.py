import datetime
import unittest
import logging

from app.generator import MedicalReportsGenerator
from app.language import Language
from data.models import Diagnosis, Discharge, Etiology, PostStrokeComplications, PostAcuteCare, Treatment, Admission, \
    Onset, Patient, Thrombolysis, Thrombectomy, MedicalReport, FollowUpImaging
from tests.definitions import FIXTURES_PATH
from utils.load_language_utils import load_json_file


class TestMedicalRecordsGenerator(unittest.TestCase):
    def setUp(self) -> None:
        language_file_path = FIXTURES_PATH / "language.json"
        data_file_path = FIXTURES_PATH / "data.json"
        path_to_template = FIXTURES_PATH / "test.txt"

        language_file = load_json_file(language_file_path)
        language = Language(**language_file)

        self.data = load_json_file(data_file_path)
        self.data["occlusion_left_mca_m1"] = True
        self.data["occlusion_right_mca_m1"] = True
        self.data["risk_diabetes"] = True
        self.data["risk_covid"] = True
        self.data["risk_atrial_fibrilation"] = True
        self.data["before_onset_cilostazol"] = True
        self.data["thrombolysis"] = True
        self.data["no_thrombolysis_reason"] = None
        self.data["door_to_needle"] = 14
        self.data["ivt_treatment"] = "alteplase"
        self.data["ivt_dose"] = 50
        self.data["thrombectomy"] = True
        self.data["no_thrombectomy_reason"] = None
        self.data["door_to_groin"] = 56
        self.data["tici_score"] = "2B"
        self.data["post_treatment_infarction"] = True
        self.data["post_stroke_pneumonia"] = True
        self.data["post_stroke_dvt"] = True
        self.data["post_stroke_sepsis"] = True
        self.data["discharge_cilostazol"] = True
        self.data["discharge_clopidrogel"] = True
        self.data["discharge_ticlopidine"] = True
        self.data["discharge_date"] = datetime.date(2022, 11, 24)
        self.data["discharge_medication"] = True
        self.generator = MedicalReportsGenerator(language, path_to_template)

    def test_replace_last(self):
        test_str = "orange, bananna, apple, strawberry"
        replacement = ", and"

        result = MedicalReportsGenerator.replace_last(test_str, ",", replacement)

        self.assertEqual("orange, bananna, apple, and strawberry", result)

    def test_prepare_scoped_values_simple(self):
        values = {"scope": {"a": 4, "b": 1}}

        result = self.generator._MedicalReportsGenerator__prepare_scoped_values(values)

        self.assertEqual({"scope.a": 4, "scope.b": 1}, result)

    def test_prepare_scoped_values_complex(self):
        values = {"scope1": {"a": 4, "b": 1},
                  "scope2": {"a": "hey", "b": 1, "c": 1564687},
                  "scope3": {"a": 2163, "b": 4324},
                  "scope4": {"a": "hey", "b": "aloha", "c": "now"}}

        result = self.generator._MedicalReportsGenerator__prepare_scoped_values(values)
        expected = {"scope1.a": 4, "scope1.b": 1,
                    "scope2.a": "hey", "scope2.b": 1, "scope2.c": 1564687,
                    "scope3.a": 2163, "scope3.b": 4324,
                    "scope4.a": "hey", "scope4.b": "aloha", "scope4.c": "now"}

        self.assertEqual(expected, result)

    def test_translate_data_empty(self):
        data = None
        key = "key"

        result = self.generator._MedicalReportsGenerator__translate_data(data, key)

        self.assertEqual("", result)

    def test_translate_data(self):
        data = {"test": "value"}
        key = "test"

        result = self.generator._MedicalReportsGenerator__translate_data(data, key)

        self.assertEqual("value", result)

    def test_translate_data_invalid(self):
        data = {"test": "value"}
        key = "invalid"

        with self.assertLogs(None, logging.ERROR):
            result = self.generator._MedicalReportsGenerator__translate_data(data, key)

        self.assertEqual("", result)

    def test_parse_data_single(self):
        data = {"test": "value"}
        translations = {"test": "changed value"}

        result = self.generator._MedicalReportsGenerator__parse_data(translations, data)

        self.assertEqual("changed value", result)

    def test_parse_data_multiple(self):
        data = {"test1": "value", "test2": "value2", "test3": "value3"}
        translations = {"test1": "changed value", "test2": "changed value2", "test3": "changed value3"}

        result = self.generator._MedicalReportsGenerator__parse_data(translations, data)

        self.assertEqual("changed value, changed value2, and changed value3", result)

    def test_get_variable_invalid(self):
        key = "invalid_key"

        with self.assertLogs(None, logging.ERROR):
            result = self.generator._MedicalReportsGenerator__get_variables(key)

        self.assertIsNone(result)

    def test_get_variable_valid(self):
        self.generator.language.variables["test"] = {}
        self.generator.language.variables["test"]["first"] = "val1"
        self.generator.language.variables["test"]["second"] = "val2"
        self.generator.language.variables["test"]["third"] = "val3"

        key = "test"

        result = self.generator._MedicalReportsGenerator__get_variables(key)
        expected = {"first": "val1", "second": "val2", "third": "val3"}

        self.assertEqual(expected, result)

    def test_get_setting_invalid(self):
        key = "invalid_key"

        with self.assertLogs(None, logging.ERROR):
            result = self.generator._MedicalReportsGenerator__get_setting(key)

        self.assertIsNone(result)

    def test_get_setting_valid(self):
        self.generator.language.settings["test1"] = "val1"
        self.generator.language.settings["test2"] = "val2"
        self.generator.language.settings["test3"] = "val3"

        key = "test1"

        result = self.generator._MedicalReportsGenerator__get_setting(key)

        self.assertEqual("val1", result)

    def test_diagnosis_empty(self):
        self.generator.data = {}

        result = self.generator._MedicalReportsGenerator__create_diagnosis()

        self.assertIsInstance(result, Diagnosis)

    def test_diagnosis_with_data(self):
        self.generator.data = self.data

        result = self.generator._MedicalReportsGenerator__create_diagnosis()

        self.assertIsInstance(result, Diagnosis)
        self.assertEqual("ischemic", result.stroke_type)
        self.assertEqual(10, result.aspects_score)
        self.assertEqual("CT CTA", result.imaging_type)
        self.assertEqual("left MCA M1, and right MCA M1", result.occlusion_position)
        self.assertIsNone(result.imaging_timestamp)
        self.assertFalse(result.imaging_within_hour)

    def test_patient_empty(self):
        self.generator.data = {}

        result = self.generator._MedicalReportsGenerator__create_patient()

        self.assertIsInstance(result, Patient)

    def test_patient_with_data(self):
        self.generator.data = self.data

        result = self.generator._MedicalReportsGenerator__create_patient()

        self.assertIsInstance(result, Patient)
        self.assertEqual(77, result.age)
        self.assertEqual("male", result.sex)
        self.assertEqual(4, result.patient_id)
        self.assertEqual("diabetes, and covid", result.risk_factors)
        self.assertEqual("cilostazol", result.prior_treatment)
        self.assertEqual("AF", result.risk_atrial_fibrilation)

    def test_onset_empty(self):
        self.generator.data = {}

        result = self.generator._MedicalReportsGenerator__create_onset()

        self.assertIsInstance(result, Onset)

    def test_onset_with_data(self):
        self.generator.data = self.data

        result = self.generator._MedicalReportsGenerator__create_onset()

        self.assertIsInstance(result, Onset)
        self.assertEqual(datetime.date(2022, 6, 10).strftime("%b %d %Y"), result.onset_date)
        self.assertEqual(datetime.time(0, 46).strftime("%H:%M%p"), result.onset_time)
        self.assertFalse(result.wake_up_stroke)

    def test_admission_empty(self):
        self.generator.data = {}

        result = self.generator._MedicalReportsGenerator__create_admission()

        self.assertIsInstance(result, Admission)

    def test_admission_with_data(self):
        self.generator.data = self.data

        result = self.generator._MedicalReportsGenerator__create_admission()

        self.assertIsInstance(result, Admission)
        self.assertEqual(9, result.admission_nihss)
        self.assertEqual(10, result.aspects_score)
        self.assertEqual("monitored bed", result.admission_type)
        self.assertEqual(0, result.prestroke_mrs)
        self.assertEqual(147, result.sys_blood_pressure)
        self.assertEqual(112, result.dia_blood_pressure)
        self.assertEqual(datetime.time(4).strftime("%H:%M%p"), result.arrival_time)
        self.assertEqual("private transportation", result.arrival_mode)
        self.assertEqual("other", result.department_type)
        self.assertIsNone(result.prenotification)

    def test_treatment_empty(self):
        self.generator.data = {}

        result = self.generator._MedicalReportsGenerator__create_treatment()

        self.assertIsInstance(result, Treatment)

    def test_treatment_with_data(self):
        self.generator.data = self.data

        result = self.generator._MedicalReportsGenerator__create_treatment()

        self.assertIsInstance(result, Treatment)
        self.assertTrue(result.thrombolysis_done)
        self.assertIsNone(result.no_thrombolysis_reasons)
        self.assertTrue(result.thrombectomy_done)
        self.assertIsNone(result.no_thrombectomy_reasons)

        with self.subTest("Thrombolysis check"):
            self.assertIsInstance(result.thrombolysis, Thrombolysis)
            self.assertEqual(14, result.thrombolysis.dtn)
            self.assertEqual("alteplase", result.thrombolysis.ivt_treatment)
            self.assertEqual(50, result.thrombolysis.ivt_dose)

        with self.subTest("Thrombectomy check"):
            self.assertIsInstance(result.thrombectomy, Thrombectomy)
            self.assertEqual(56, result.thrombectomy.dtg)
            self.assertIsNone(result.thrombectomy.dio)
            self.assertEqual("2B", result.thrombectomy.tici_score)
            self.assertEqual("tici_score_2B", result.thrombectomy.tici_score_meaning)

    def test_post_treatment_imaging_empty(self):
        self.generator.data = {}

        result = self.generator._MedicalReportsGenerator__create_follow_up_imaging()

        self.assertIsInstance(result, FollowUpImaging)

    def test_post_treatment_imaging_with_data(self):
        self.generator.data = self.data

        result = self.generator._MedicalReportsGenerator__create_follow_up_imaging()

        self.assertIsInstance(result, FollowUpImaging)
        self.assertEqual("no", result.imaging_type)
        self.assertEqual("brain infarct", result.findings)

    def test_post_acute_care_empty(self):
        self.generator.data = {}

        result = self.generator._MedicalReportsGenerator__create_post_acute_care()

        self.assertIsInstance(result, PostAcuteCare)

    def test_post_acute_care_with_data(self):
        self.generator.data = self.data

        result = self.generator._MedicalReportsGenerator__create_post_acute_care()

        self.assertIsInstance(result, PostAcuteCare)
        self.assertEqual("no AF", result.afib_flutter)
        self.assertEqual("yes", result.swallowing_screening)
        self.assertEqual("other", result.swallowing_screening_type)
        self.assertTrue(result.physiotherapy)
        self.assertFalse(result.ergotherapy)
        self.assertTrue(result.speechtherapy)
        self.assertEqual("physiotherapy, and speechtherapy", result.therapies)

    def test_post_stroke_complications_empty(self):
        self.generator.data = {}

        result = self.generator._MedicalReportsGenerator__create_post_stroke_complications()

        self.assertIsInstance(result, PostStrokeComplications)

    def test_post_stroke_complications_with_data(self):
        self.generator.data = self.data

        result = self.generator._MedicalReportsGenerator__create_post_stroke_complications()
        expected = "pneumonia, deep vein thrombosis (DVT), and drip site sepsis"

        self.assertIsInstance(result, PostStrokeComplications)
        self.assertEqual(expected, result.complications)

    def test_etiology_empty(self):
        self.generator.data = {}

        result = self.generator._MedicalReportsGenerator__create_etiology()

        self.assertIsInstance(result, Etiology)

    def test_etiology_with_data(self):
        self.generator.data = self.data

        result = self.generator._MedicalReportsGenerator__create_etiology()

        self.assertIsInstance(result, Etiology)
        self.assertTrue(result.large_artery)
        self.assertFalse(result.cardioembolism)
        self.assertFalse(result.cryptogenic_stroke)
        self.assertFalse(result.small_vessel)
        self.assertFalse(result.other)
        self.assertTrue(result.carotid_stenosis)
        self.assertEqual("over 70", result.carotid_stenosis_level)
        self.assertEqual("no AF", result.afib_flutter)

    def test_discharge_empty(self):
        self.generator.data = {}

        result = self.generator._MedicalReportsGenerator__create_discharge()

        self.assertIsInstance(result, Discharge)

    def test_discharge_with_data(self):
        self.generator.data = self.data

        result = self.generator._MedicalReportsGenerator__create_discharge()

        self.assertIsInstance(result, Discharge)
        self.assertEqual(datetime.date(2022, 11, 24).strftime("%b %d %Y"), result.discharge_date)
        self.assertEqual("home", result.discharge_destination)
        self.assertEqual(2, result.nihss)
        self.assertEqual(1, result.discharge_mrs)
        self.assertIsNone(result.contact_date)
        self.assertEqual("not contacted", result.mode_contact)
        self.assertEqual("cilostazol, clopidrogel, and ticlopidine", result.discharge_medication)

    def test_create_medical_record(self):
        result = self.generator._MedicalReportsGenerator__create_medical_report()

        self.assertIsInstance(result, MedicalReport)
        self.assertIsInstance(result.diagnosis, Diagnosis)
        self.assertIsInstance(result.patient, Patient)
        self.assertIsInstance(result.onset, Onset)
        self.assertIsInstance(result.admission, Admission)
        self.assertIsInstance(result.treatment, Treatment)
        self.assertIsInstance(result.post_acute_care, PostAcuteCare)
        self.assertIsInstance(result.post_stroke_complications, PostStrokeComplications)
        self.assertIsInstance(result.etiology, Etiology)
        self.assertIsInstance(result.discharge, Discharge)

    def test_generate_structure(self):
        self.generator.data = self.data

        result = self.generator._MedicalReportsGenerator__generate_structure()
        expected = {"diagnosis": "Diagnosis test with CT CTA variable",
                    "patient": "Test patient whose sex is not other M/77",
                    "onset": "Onset on Jun 10 2022. ",
                    "admission": "ASPECT score 10. ",
                    "treatment": "Treatment showing dtg 56",
                    "follow_up_imaging": "",
                    "post_acute_care": "Received physiotherapy, and speechtherapy. ",
                    "post_stroke_complications": "Post stroke complications: "
                                                 "pneumonia, deep vein thrombosis (DVT), and drip site sepsis. ",
                    "etiology": "",
                    "discharge": "Medication: cilostazol, clopidrogel, and ticlopidine. "}

        self.assertEqual(expected, result)

    def test_generate_medical_record(self):
        result = self.generator.generate_medical_report(self.data)
        expected = "Diagnosis test with CT CTA variableTest patient whose sex is not other M/77Onset on Jun 10 2022. " \
                   "ASPECT score 10. Treatment showing dtg 56Received physiotherapy, and speechtherapy. " \
                   "Post stroke complications: pneumonia, deep vein thrombosis (DVT), and drip site sepsis. " \
                   "Medication: cilostazol, clopidrogel, and ticlopidine. "

        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
