import unittest

import medicalrecordgenerator.app.parser as parser


class TestParser(unittest.TestCase):
    def test_and_true(self):
        test_json = {"type": "AND", "conditions": [{"type": "EXISTENCE",
                                                    "scope": "a",
                                                    "value": True},
                                                   {"type": "EXISTENCE",
                                                    "scope": "b",
                                                    "value": True}]}
        data = {"b": "test", "a": 4}
        self.assertTrue(parser.parse_and(test_json, data))

    def test_and_false(self):
        test_json = {"type": "AND", "conditions": [{"type": "EXISTENCE",
                                                    "scope": "a",
                                                    "value": True},
                                                   {"type": "EXISTENCE",
                                                    "scope": "b",
                                                    "value": False}]}
        data = {"b": "test", "a": 4}
        self.assertFalse(parser.parse_and(test_json, data))

    def test_or_true(self):
        test_json = {"type": "OR", "conditions": [{"type": "EXISTENCE",
                                                   "scope": "a",
                                                   "value": False},
                                                  {"type": "EXISTENCE",
                                                   "scope": "b",
                                                   "value": True}]}
        data = {"b": "test", "a": 4}
        self.assertTrue(parser.parse_or(test_json, data))

    def test_or_false(self):
        test_json = {"type": "OR", "conditions": [{"type": "EXISTENCE",
                                                   "scope": "a",
                                                   "value": False},
                                                  {"type": "EXISTENCE",
                                                   "scope": "b",
                                                   "value": False}]}
        data = {"b": "test", "a": 4}
        self.assertFalse(parser.parse_or(test_json, data))

    def test_not_true(self):
        test_json = {"type": "NOT", "conditions": [{"type": "EXISTENCE",
                                                    "scope": "a",
                                                    "value": False},
                                                   {"type": "EXISTENCE",
                                                    "scope": "b",
                                                    "value": False}]}
        data = {"b": "test", "a": 4}
        self.assertTrue(parser.parse_not(test_json, data))

    def test_not_false(self):
        test_json = {"type": "NOT", "conditions": [{"type": "EXISTENCE",
                                                    "scope": "a",
                                                    "value": True}]}
        data = {"a": 4}
        self.assertFalse(parser.parse_not(test_json, data))

    def test_value_num_1(self):
        test_json = {"type": "VALUE",
                     "scope": "a",
                     "value": 4}

        data = {"a": 4}
        self.assertTrue(parser.parse_value(test_json, data))

    def test_value_num_2(self):
        test_json = {"type": "VALUE",
                     "scope": "a",
                     "value": 3}

        data = {"a": 4}
        self.assertFalse(parser.parse_value(test_json, data))

    def test_value_bool_1(self):
        test_json = {"type": "VALUE",
                     "scope": "a",
                     "value": False}

        data = {"a": False}
        self.assertTrue(parser.parse_value(test_json, data))

    def test_value_bool_2(self):
        test_json = {"type": "VALUE",
                     "scope": "a",
                     "value": True}

        data = {"a": False}
        self.assertFalse(parser.parse_value(test_json, data))

    def test_existence_num_1(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "a",
                     "value": True}

        data = {"a": 1}
        self.assertTrue(parser.parse_existence(test_json, data))

    def test_existence_bool_1(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "a",
                     "value": True}

        data = {"a": True}
        self.assertTrue(parser.parse_existence(test_json, data))

    def test_existence_str_1(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "a",
                     "value": True}

        data = {"a": "aloha"}
        self.assertTrue(parser.parse_existence(test_json, data))

    def test_existence_str_2(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "a",
                     "value": False}

        data = {"a": ""}
        self.assertTrue(parser.parse_existence(test_json, data))

    def test_existence_str_3(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "a",
                     "value": False}

        data = {"a": ""}
        self.assertTrue(parser.parse_existence(test_json, data))

    def test_existence_str_4(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "a",
                     "value": False}

        data = {"a": "aloha"}
        self.assertFalse(parser.parse_existence(test_json, data))

    def test_existence_str_5(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "a",
                     "value": True}

        data = {"a": ""}
        self.assertFalse(parser.parse_existence(test_json, data))

    def test_existence_none_1(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "a",
                     "value": False}

        data = {"a": None}
        self.assertTrue(parser.parse_existence(test_json, data))

    def test_existence_none_2(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "a",
                     "value": True}

        data = {"a": None}
        self.assertFalse(parser.parse_existence(test_json, data))


if __name__ == '__main__':
    unittest.main()
