import unittest

import medicalrecordgenerator.app.parser as parser


class TestParser(unittest.TestCase):
    def test_and_true(self):
        test_json = {"type": "AND", "conditions": [{"type": "EXISTENCE",
                                                    "scope": "ivt_dose",
                                                    "value": True},
                                                   {"type": "EXISTENCE",
                                                    "scope": "ivt_treatment",
                                                    "value": True}]}
        data = {"ivt_treatment": "alteplase", "ivt_dose": 4}
        self.assertTrue(parser.parse_and(test_json, data))

    def test_and_false(self):
        test_json = {"type": "AND", "conditions": [{"type": "EXISTENCE",
                                                    "scope": "ivt_dose",
                                                    "value": True},
                                                   {"type": "EXISTENCE",
                                                    "scope": "ivt_treatment",
                                                    "value": False}]}
        data = {"ivt_treatment": "alteplase", "ivt_dose": 4}
        self.assertFalse(parser.parse_and(test_json, data))

    def test_or_true(self):
        test_json = {"type": "OR", "conditions": [{"type": "EXISTENCE",
                                                   "scope": "ivt_dose",
                                                   "value": False},
                                                  {"type": "EXISTENCE",
                                                   "scope": "ivt_treatment",
                                                   "value": True}]}
        data = {"ivt_treatment": "alteplase", "ivt_dose": 4}
        self.assertTrue(parser.parse_or(test_json, data))

    def test_or_false(self):
        test_json = {"type": "OR", "conditions": [{"type": "EXISTENCE",
                                                   "scope": "ivt_dose",
                                                   "value": False},
                                                  {"type": "EXISTENCE",
                                                   "scope": "ivt_treatment",
                                                   "value": False}]}
        data = {"ivt_treatment": "alteplase", "ivt_dose": 4}
        self.assertFalse(parser.parse_or(test_json, data))


if __name__ == '__main__':
    unittest.main()
