import logging
import unittest

from app.language import Condition, ConditionEmpty, ConditionValue, ConditionExistence, ConditionAnd, ConditionOr, \
    ConditionNot


class TestCondition(unittest.TestCase):
    def test_parse_empty(self):
        data = {}
        condition = Condition.parse_condition(data)

        self.assertIsInstance(condition, ConditionEmpty)

    def test_parse_value(self):
        data = {"type": "VALUE",
                "scope": "test_scope",
                "value": "test_value"}
        condition = Condition.parse_condition(data)

        self.assertIsInstance(condition, ConditionValue)
        self.assertEqual("test_scope", condition.scope)
        self.assertEqual("test_value", condition.value)

    def test_parse_existence(self):
        data = {"type": "EXISTENCE",
                "scope": "test_scope",
                "value": "test_value"}
        condition = Condition.parse_condition(data)

        self.assertIsInstance(condition, ConditionExistence)
        self.assertEqual("test_scope", condition.scope)
        self.assertEqual("test_value", condition.value)

    def test_parse_list_empty(self):
        data = []
        condition = Condition()
        conditions = condition.parse_conditions(data)

        self.assertEqual(len(conditions), 0)
        self.assertEqual(conditions, [])

    def test_parse_list_single(self):
        data = [{"type": "EXISTENCE", "scope": "test_scope", "value": "test_value"}]
        condition = Condition()
        conditions = condition.parse_conditions(data)

        self.assertEqual(len(conditions), 1)
        self.assertIsInstance(conditions[0], ConditionExistence)

    def test_parse_list_multiple(self):
        data = [{"type": "EXISTENCE", "scope": "test_scope", "value": "test_value"},
                {"type": "VALUE", "scope": "test_scope2", "value": "test_value2"},
                {}]
        condition = Condition()
        conditions = condition.parse_conditions(data)

        self.assertEqual(len(conditions), 3)

        self.assertIsInstance(conditions[0], ConditionExistence)
        self.assertEqual("test_scope", conditions[0].scope)
        self.assertEqual("test_value", conditions[0].value)

        self.assertIsInstance(conditions[1], ConditionValue)
        self.assertEqual("test_scope2", conditions[1].scope)
        self.assertEqual("test_value2", conditions[1].value)

        self.assertIsInstance(conditions[2], ConditionEmpty)

    def test_parse_and(self):
        data = {"type": "AND",
                "conditions": [{"type": "EXISTENCE", "scope": "test_scope", "value": "test_value"}]}
        condition = Condition.parse_condition(data)

        self.assertIsInstance(condition, ConditionAnd)
        self.assertEqual(len(condition.conditions), 1)
        self.assertIsInstance(condition.conditions[0], ConditionExistence)

    def test_parse_or(self):
        data = {"type": "OR",
                "conditions": [{"type": "VALUE", "scope": "test_scope", "value": "test_value"}]}
        condition = Condition.parse_condition(data)

        self.assertIsInstance(condition, ConditionOr)
        self.assertEqual(len(condition.conditions), 1)
        self.assertIsInstance(condition.conditions[0], ConditionValue)

    def test_parse_not(self):
        data = {"type": "NOT",
                "conditions": [{"type": "EXISTENCE", "scope": "test_scope", "value": "test_value"}]}
        condition = Condition.parse_condition(data)

        self.assertIsInstance(condition, ConditionNot)
        self.assertEqual(len(condition.conditions), 1)
        self.assertIsInstance(condition.conditions[0], ConditionExistence)

    def test_parse_throws(self):
        data = {"type": "EXISTENCE", "scope": "test_scope", "": "test_value"}

        with self.assertRaises(AttributeError):
            Condition.parse_condition(data)


class TestConditionValue(unittest.TestCase):
    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

    def test_result_true_str(self):
        condition = ConditionValue("scope.test", "value")
        data = {"scope": {"test": "value"}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_result_true_int(self):
        condition = ConditionValue("scope.test", 16)
        data = {"scope": {"test": 16}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_result_false(self):
        condition = ConditionValue("scope.test", "value")
        data = {"scope": {"test": "val"}}

        result = condition.get_condition_result(data)

        self.assertFalse(result)

    def test_result_attribute_error(self):
        condition = ConditionValue(None, "value")
        data = {"scope": {"test": "value"}}

        with self.assertRaises(AttributeError):
            condition.get_condition_result(data)

    def test_result_value_error(self):
        condition = ConditionValue("scope", "value")
        data = {"scope": {"test": "value"}}

        with self.assertRaises(ValueError):
            condition.get_condition_result(data)

    def test_result_key_error(self):
        condition = ConditionValue("scope.test", "value")
        data = {"scope": {"": "value"}}

        with self.assertRaises(KeyError):
            condition.get_condition_result(data)


class TestConditionExistence(unittest.TestCase):
    def setUp(self) -> None:
        logging.disable(logging.CRITICAL)

    def test_result_true_bool_existing(self):
        condition = ConditionExistence("scope.test", True)
        data = {"scope": {"test": True}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_result_true_bool_not_existing(self):
        condition = ConditionExistence("scope.test", False)
        data = {"scope": {"test": False}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_result_true_str_existing(self):
        condition = ConditionExistence("scope.test", True)
        data = {"scope": {"test": "value"}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_result_true_str_not_existing(self):
        condition = ConditionExistence("scope.test", False)
        data = {"scope": {"test": ""}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_result_true_int_existing(self):
        condition = ConditionExistence("scope.test", True)
        data = {"scope": {"test": 16}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_result_false_bool_existing(self):
        condition = ConditionExistence("scope.test", True)
        data = {"scope": {"test": False}}

        result = condition.get_condition_result(data)

        self.assertFalse(result)

    def test_result_false_bool_not_existing(self):
        condition = ConditionExistence("scope.test", False)
        data = {"scope": {"test": True}}

        result = condition.get_condition_result(data)

        self.assertFalse(result)

    def test_result_false_str_existing(self):
        condition = ConditionExistence("scope.test", True)
        data = {"scope": {"test": ""}}

        result = condition.get_condition_result(data)

        self.assertFalse(result)

    def test_result_false_str_not_existing(self):
        condition = ConditionExistence("scope.test", False)
        data = {"scope": {"test": "value"}}

        result = condition.get_condition_result(data)

        self.assertFalse(result)

    def test_result_attribute_error(self):
        condition = ConditionExistence(None, True)
        data = {"scope": {"test": "value"}}

        with self.assertRaises(AttributeError):
            condition.get_condition_result(data)

    def test_result_value_error(self):
        condition = ConditionExistence("scope", True)
        data = {"scope": {"test": 1}}

        with self.assertRaises(ValueError):
            condition.get_condition_result(data)

    def test_result_key_error(self):
        condition = ConditionExistence("scope.test", True)
        data = {"scope": {"": "value"}}

        with self.assertRaises(KeyError):
            condition.get_condition_result(data)


class TestConditionAnd(unittest.TestCase):
    def test_and_true_simple(self):
        condition = ConditionAnd([{"type": "EXISTENCE", "scope": "scope.a", "value": True},
                                  {"type": "VALUE", "scope": "scope.b", "value": 4}])
        data = {"scope": {"a": "test", "b": 4}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_and_true_complex(self):
        condition = ConditionAnd([{"type": "EXISTENCE", "scope": "scope.a", "value": True},
                                  {"type": "VALUE", "scope": "scope.b", "value": 4},
                                  {"type": "AND",
                                   "conditions": [{"type": "VALUE", "scope": "scope2.a", "value": "aloha"},
                                                  {"type": "VALUE", "scope": "scope2.b", "value": 6.87}]}])
        data = {"scope": {"a": "test", "b": 4}, "scope2": {"a": "aloha", "b": 6.87}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_and_false_simple(self):
        condition = ConditionAnd([{"type": "EXISTENCE", "scope": "scope.a", "value": True},
                                  {"type": "VALUE", "scope": "scope.b", "value": 1}])
        data = {"scope": {"a": "test", "b": 4}}

        result = condition.get_condition_result(data)

        self.assertFalse(result)

    def test_and_false_complex(self):
        condition = ConditionAnd([{"type": "EXISTENCE", "scope": "scope.a", "value": True},
                                  {"type": "VALUE", "scope": "scope.b", "value": 4},
                                  {"type": "AND",
                                   "conditions": [{"type": "VALUE", "scope": "scope2.a", "value": "aloha"},
                                                  {"type": "VALUE", "scope": "scope2.b", "value": 6.87}]}])
        data = {"scope": {"a": "test", "b": 4}, "scope2": {"a": "hello", "b": 6.87}}

        result = condition.get_condition_result(data)

        self.assertFalse(result)


class TestConditionOr(unittest.TestCase):
    def test_or_true_simple(self):
        condition = ConditionOr([{"type": "EXISTENCE", "scope": "scope.a", "value": True},
                                 {"type": "VALUE", "scope": "scope.b", "value": 4}])
        data = {"scope": {"a": "Test", "b": 1}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_or_true_complex(self):
        condition = ConditionOr([{"type": "EXISTENCE", "scope": "scope.a", "value": False},
                                 {"type": "VALUE", "scope": "scope.b", "value": 4},
                                 {"type": "OR",
                                  "conditions": [{"type": "VALUE", "scope": "scope2.a", "value": "aloha"},
                                                 {"type": "VALUE", "scope": "scope2.b", "value": 6.87}]}])
        data = {"scope": {"a": "test", "b": 1}, "scope2": {"a": "aloha", "b": 5.17}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_or_false_simple(self):
        condition = ConditionOr([{"type": "EXISTENCE", "scope": "scope.a", "value": False},
                                 {"type": "VALUE", "scope": "scope.b", "value": 1}])
        data = {"scope": {"a": "test", "b": 4}}

        result = condition.get_condition_result(data)

        self.assertFalse(result)

    def test_or_false_complex(self):
        condition = ConditionOr([{"type": "EXISTENCE", "scope": "scope.a", "value": False},
                                 {"type": "VALUE", "scope": "scope.b", "value": 4},
                                 {"type": "AND",
                                  "conditions": [{"type": "VALUE", "scope": "scope2.a", "value": "aloha"},
                                                 {"type": "VALUE", "scope": "scope2.b", "value": 6.87}]}])
        data = {"scope": {"a": "test", "b": 1}, "scope2": {"a": "hello", "b": 5.17}}

        result = condition.get_condition_result(data)

        self.assertFalse(result)


class TestConditionNot(unittest.TestCase):
    def test_not_true_simple(self):
        condition = ConditionNot([{"type": "VALUE", "scope": "scope.a", "value": 4}])

        data = {"scope": {"a": 1}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_not_true_complex(self):
        condition = ConditionNot([{"type": "EXISTENCE", "scope": "scope.a", "value": False},
                                  {"type": "VALUE", "scope": "scope.b", "value": 4}])

        data = {"scope": {"a": "aloha", "b": 1}}

        result = condition.get_condition_result(data)

        self.assertTrue(result)

    def test_not_false_simple(self):
        condition = ConditionNot([{"type": "VALUE", "scope": "scope.a", "value": 4}])

        data = {"scope": {"a": 4}}

        result = condition.get_condition_result(data)

        self.assertFalse(result)

    def test_not_false_complex(self):
        condition = ConditionNot([{"type": "EXISTENCE", "scope": "scope.a", "value": True},
                                  {"type": "VALUE", "scope": "scope.b", "value": 4}])

        data = {"scope": {"a": "test", "b": 4}}

        result = condition.get_condition_result(data)

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
