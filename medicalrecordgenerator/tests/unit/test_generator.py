import datetime
import unittest
import logging

from app.generator import MedicalRecordsGenerator
from app.language import Language
from data.models import Diagnosis, Discharge, Etiology, PostStrokeComplications, PostAcuteCare, Treatment, Admission, \
    Onset, Patient
from utils.load_utils import load_language_file


class TestMedicalRecordsGenerator(unittest.TestCase):
    def setUp(self) -> None:
        language_file = load_language_file("fixtures/language.json")
        language = Language(**language_file)

        self.data = load_language_file("fixtures/data.json")
        self.generator = MedicalRecordsGenerator(language, {})

    def test_replace_last(self):
        test_str = "orange, bananna, apple, strawberry"
        replacement = ", and"

        result = MedicalRecordsGenerator.replace_last(test_str, ",", replacement)

        self.assertEqual("orange, bananna, apple, and strawberry", result)

    def test_prepare_scoped_values_simple(self):
        values = {"scope": {"a": 4, "b": 1}}

        result = MedicalRecordsGenerator.prepare_scoped_values(values)

        self.assertEqual({"scope.a": 4, "scope.b": 1}, result)

    def test_prepare_scoped_values_complex(self):
        values = {"scope1": {"a": 4, "b": 1},
                  "scope2": {"a": "hey", "b": 1, "c": 1564687},
                  "scope3": {"a": 2163, "b": 4324},
                  "scope4": {"a": "hey", "b": "aloha", "c": "now"}}

        result = MedicalRecordsGenerator.prepare_scoped_values(values)
        expected = {"scope1.a": 4, "scope1.b": 1,
                    "scope2.a": "hey", "scope2.b": 1, "scope2.c": 1564687,
                    "scope3.a": 2163, "scope3.b": 4324,
                    "scope4.a": "hey", "scope4.b": "aloha", "scope4.c": "now"}

        self.assertEqual(expected, result)

    def test_translate_data_empty(self):
        data = None
        key = "key"

        result = MedicalRecordsGenerator.translate_data(data, key)

        self.assertEqual("", result)

    def test_translate_data(self):
        data = {"test": "value"}
        key = "test"

        result = MedicalRecordsGenerator.translate_data(data, key)

        self.assertEqual("value", result)

    def test_translate_data_invalid(self):
        data = {"test": "value"}
        key = "invalid"

        with self.assertLogs(None, logging.ERROR):
            result = MedicalRecordsGenerator.translate_data(data, key)

        self.assertEqual("", result)

    def test_parse_data_single(self):
        data = {"test": "value"}
        translations = {"test": "changed value"}

        result = self.generator.parse_data(translations, data)

        self.assertEqual("changed value", result)

    def test_parse_data_multiple(self):
        data = {"test1": "value", "test2": "value2", "test3": "value3"}
        translations = {"test1": "changed value", "test2": "changed value2", "test3": "changed value3"}

        result = self.generator.parse_data(translations, data)

        self.assertEqual("changed value, changed value2, and changed value3", result)

    def test_get_variable_invalid(self):
        key = "invalid_key"

        with self.assertLogs(None, logging.ERROR):
            result = self.generator.get_variables(key)

        self.assertIsNone(result)

    def test_get_variable_valid(self):
        self.generator.language.variables["test"] = {}
        self.generator.language.variables["test"]["first"] = "val1"
        self.generator.language.variables["test"]["second"] = "val2"
        self.generator.language.variables["test"]["third"] = "val3"

        key = "test"

        result = self.generator.get_variables(key)
        expected = {"first": "val1", "second": "val2", "third": "val3"}

        self.assertEqual(expected, result)

    def test_get_setting_invalid(self):
        key = "invalid_key"

        with self.assertLogs(None, logging.ERROR):
            result = self.generator.get_setting(key)

        self.assertIsNone(result)

    def test_get_setting_valid(self):
        self.generator.language.settings["test1"] = "val1"
        self.generator.language.settings["test2"] = "val2"
        self.generator.language.settings["test3"] = "val3"

        key = "test1"

        result = self.generator.get_setting(key)

        self.assertEqual("val1", result)

    def test_diagnosis_empty(self):
        self.generator.data = {}

        result = self.generator.create_diagnosis()

        self.assertIsInstance(result, Diagnosis)

    def test_diagnosis_with_data(self):
        self.data["occlusion_left_mca_m1"] = True
        self.data["occlusion_right_mca_m1"] = True
        self.generator.data = self.data

        self.generator.language.variables["occlusion_position"]["occlusion_left_mca_m1"] = "left MCA M1"
        self.generator.language.variables["occlusion_position"]["occlusion_right_mca_m1"] = "right MCA M1"

        result = self.generator.create_diagnosis()

        self.assertIsInstance(result, Diagnosis)
        self.assertEqual("ischemic", result.stroke_type)
        self.assertEqual(10, result.aspects_score)
        self.assertEqual("CT CTA", result.imaging_type)
        self.assertEqual("left MCA M1, and right MCA M1", result.occlusion_position)
        self.assertIsNone(result.imaging_timestamp)
        self.assertFalse(result.imaging_within_hour)

    def test_patient_empty(self):
        self.generator.data = {}

        result = self.generator.create_patient()

        self.assertIsInstance(result, Patient)

    def test_patient_with_data(self):
        self.data["risk_diabetes"] = True
        self.data["risk_covid"] = True
        self.data["risk_atrial_fibrilation"] = True
        self.data["before_onset_cilostazol"] = True
        self.generator.data = self.data

        self.generator.language.variables["risk_factors"]["risk_diabetes"] = "diabetes"
        self.generator.language.variables["risk_factors"]["risk_covid"] = "covid"
        self.generator.language.variables["risk_factors"]["risk_atrial_fibrilation"] = "AF"
        self.generator.language.variables["prior_treatment"]["before_onset_cilostazol"] = "cilostazol"

        result = self.generator.create_patient()

        self.assertIsInstance(result, Patient)
        self.assertEqual(77, result.age)
        self.assertEqual("male", result.sex)
        self.assertEqual(4, result.patient_id)
        self.assertEqual("diabetes, and covid", result.risk_factors)
        self.assertEqual("cilostazol", result.prior_treatment)
        self.assertEqual("AF", result.risk_atrial_fibrilation)

    def test_onset_empty(self):
        self.generator.data = {}

        result = self.generator.create_onset()

        self.assertIsInstance(result, Onset)

    def test_onset_with_data(self):
        self.generator.data = self.data

        result = self.generator.create_onset()

        self.assertIsInstance(result, Onset)
        self.assertEqual(datetime.date(2022, 6, 10).strftime("%b %d %Y"), result.onset_date)
        self.assertEqual(datetime.time(0, 46).strftime("%H:%M%p"), result.onset_time)
        self.assertFalse(result.wake_up_stroke)

    def test_admission_empty(self):
        self.generator.data = {}

        result = self.generator.create_admission()

        self.assertIsInstance(result, Admission)

    def test_admission_with_data(self):
        self.generator.data = self.data

        result = self.generator.create_admission()

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

        result = self.generator.create_treatment()

        self.assertIsInstance(result, Treatment)

    def test_treatment_with_data(self):
        pass

    def test_post_acute_care_empty(self):
        self.generator.data = {}

        result = self.generator.create_post_acute_care()

        self.assertIsInstance(result, PostAcuteCare)

    def test_post_acute_care_with_data(self):
        pass

    def test_post_stroke_complications_empty(self):
        self.generator.data = {}

        result = self.generator.create_post_stroke_complications()

        self.assertIsInstance(result, PostStrokeComplications)

    def test_post_stroke_complications_with_data(self):
        pass

    def test_etiology_empty(self):
        self.generator.data = {}

        result = self.generator.create_etiology()

        self.assertIsInstance(result, Etiology)

    def test_etiology_with_data(self):
        pass

    def test_discharge_empty(self):
        self.generator.data = {}

        result = self.generator.create_discharge()

        self.assertIsInstance(result, Discharge)

    def test_discharge_with_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
