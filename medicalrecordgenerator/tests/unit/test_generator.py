import unittest
import logging

from app.generator import MedicalRecordsGenerator
from app.language import Language


class TestMedicalRecordsGenerator(unittest.TestCase):
    def setUp(self) -> None:
        # TODO: Create instance of generator
        pass

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

    # def test_parse_data_single(self):
    #     data = {"test": "value"}
    #     translations = {"test": "changed value"}
    #
    #     result = MedicalRecordsGenerator.parse_data(translations, data)
    #
    #     self.assertEqual("changed value", result)


if __name__ == '__main__':
    unittest.main()
