import unittest

from old.parser import Parser


class TestParser(unittest.TestCase):
    parser = Parser({})

    def test_and_true(self):
        test_json = {"type": "AND", "conditions": [{"type": "EXISTENCE",
                                                    "scope": "scope.a",
                                                    "value": True},
                                                   {"type": "EXISTENCE",
                                                    "scope": "scope.b",
                                                    "value": True}]}
        data = {"scope": {"b": "test", "a": 4}}
        self.parser.data = data
        self.assertTrue(self.parser.parse_and(test_json))

    def test_and_false(self):
        test_json = {"type": "AND", "conditions": [{"type": "EXISTENCE",
                                                    "scope": "scope.a",
                                                    "value": True},
                                                   {"type": "EXISTENCE",
                                                    "scope": "scope.b",
                                                    "value": False}]}
        data = {"scope": {"b": "test", "a": 4}}
        self.parser.data = data
        self.assertFalse(self.parser.parse_and(test_json))

    def test_or_true(self):
        test_json = {"type": "OR", "conditions": [{"type": "EXISTENCE",
                                                   "scope": "scope.a",
                                                   "value": False},
                                                  {"type": "EXISTENCE",
                                                   "scope": "scope.b",
                                                   "value": True}]}
        data = {"scope": {"b": "test", "a": 4}}
        self.parser.data = data
        self.assertTrue(self.parser.parse_or(test_json))

    def test_or_false(self):
        test_json = {"type": "OR", "conditions": [{"type": "EXISTENCE",
                                                   "scope": "scope.a",
                                                   "value": False},
                                                  {"type": "EXISTENCE",
                                                   "scope": "scope.b",
                                                   "value": False}]}
        data = {"scope": {"b": "test", "a": 4}}
        self.parser.data = data
        self.assertFalse(self.parser.parse_or(test_json))

    def test_not_true(self):
        test_json = {"type": "NOT", "conditions": [{"type": "EXISTENCE",
                                                    "scope": "scope.a",
                                                    "value": False},
                                                   {"type": "EXISTENCE",
                                                    "scope": "scope.b",
                                                    "value": False}]}
        data = {"scope": {"b": "test", "a": 4}}
        self.parser.data = data
        self.assertTrue(self.parser.parse_not(test_json))

    def test_not_false(self):
        test_json = {"type": "NOT", "conditions": [{"type": "EXISTENCE",
                                                    "scope": "scope.a",
                                                    "value": True}]}
        data = {"scope": {"a": 4}}
        self.parser.data = data
        self.assertFalse(self.parser.parse_not(test_json))

    def test_value_num_1(self):
        test_json = {"type": "VALUE",
                     "scope": "scope.a",
                     "value": 4}

        data = {"scope": {"a": 4}}
        self.parser.data = data
        self.assertTrue(self.parser.parse_value(test_json))

    def test_value_num_2(self):
        test_json = {"type": "VALUE",
                     "scope": "scope.a",
                     "value": 3}

        data = {"scope": {"a": 4}}
        self.parser.data = data
        self.assertFalse(self.parser.parse_value(test_json))

    def test_value_bool_1(self):
        test_json = {"type": "VALUE",
                     "scope": "scope.a",
                     "value": False}

        data = {"scope": {"a": False}}
        self.parser.data = data
        self.assertTrue(self.parser.parse_value(test_json))

    def test_value_bool_2(self):
        test_json = {"type": "VALUE",
                     "scope": "scope.a",
                     "value": True}

        data = {"scope": {"a": False}}
        self.parser.data = data
        self.assertFalse(self.parser.parse_value(test_json))

    def test_existence_num_1(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "scope.a",
                     "value": True}

        data = {"scope": {"a": 1}}
        self.parser.data = data
        self.assertTrue(self.parser.parse_existence(test_json))

    def test_existence_bool_1(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "scope.a",
                     "value": True}

        data = {"scope": {"a": True}}
        self.parser.data = data
        self.assertTrue(self.parser.parse_existence(test_json))

    def test_existence_str_1(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "scope.a",
                     "value": True}

        data = {"scope": {"a": "aloha"}}
        self.parser.data = data
        self.assertTrue(self.parser.parse_existence(test_json))

    def test_existence_str_2(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "scope.a",
                     "value": False}

        data = {"scope": {"a": ""}}
        self.parser.data = data
        self.assertTrue(self.parser.parse_existence(test_json))

    def test_existence_str_3(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "scope.a",
                     "value": False}

        data = {"scope": {"a": ""}}
        self.parser.data = data
        self.assertTrue(self.parser.parse_existence(test_json))

    def test_existence_str_4(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "scope.a",
                     "value": False}

        data = {"scope": {"a": "aloha"}}
        self.parser.data = data
        self.assertFalse(self.parser.parse_existence(test_json))

    def test_existence_str_5(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "scope.a",
                     "value": True}

        data = {"scope": {"a": ""}}
        self.parser.data = data
        self.assertFalse(self.parser.parse_existence(test_json))

    def test_existence_none_1(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "scope.a",
                     "value": False}

        data = {"scope": {"a": None}}
        self.parser.data = data
        self.assertTrue(self.parser.parse_existence(test_json))

    def test_existence_none_2(self):
        test_json = {"type": "EXISTENCE",
                     "scope": "scope.a",
                     "value": True}

        data = {"scope": {"a": None}}
        self.parser.data = data
        self.assertFalse(self.parser.parse_existence(test_json))


if __name__ == '__main__':
    unittest.main()
