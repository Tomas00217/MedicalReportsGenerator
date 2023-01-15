import logging

from datetime import time

from medicalrecordgenerator.data.data_objects import ConditionType


class Parser:
    def __init__(self, data: dict):
        self.data = data

    def parse(self, dictionary: dict) -> str:
        text = ""

        try:
            variants = dictionary["variants"]
        except KeyError:
            logging.error("Invalid key, try 'variants'")
            return text

        for variant in variants:
            condition = list(variant.values())[0]
            rest = list(variant.values())[1]
            if self.parse_condition(condition, True):
                if type(rest) is dict:
                    text += self.parse(rest)
                else:
                    text += rest

        return text

    def parse_condition(self, condition: dict, is_true: bool) -> bool:
        if len(condition.keys()) == 0:
            return True

        try:
            condition_type = condition["type"]
        except KeyError:
            logging.error("Invalid condition key for %s, try 'type'", condition)
            raise

        if condition_type == ConditionType.Value.value:
            is_true = is_true and self.parse_value(condition)
        elif condition_type == ConditionType.Existence.value:
            is_true = is_true and self.parse_existence(condition)
        elif condition_type == ConditionType.And.value:
            is_true = is_true and self.parse_and(condition)
        elif condition_type == ConditionType.Or.value:
            is_true = is_true and self.parse_or(condition)
        elif condition_type == ConditionType.Not.value:
            is_true = is_true and self.parse_not(condition)

        return is_true

    def parse_value(self, condition: dict) -> bool:
        try:
            scope, variable = condition["scope"].split(".")
        except (KeyError, ValueError):
            logging.error("Invalid 'scope' key for condition")
            raise

        try:
            value = condition["value"]
        except KeyError:
            logging.error("Invalid 'value' key for condition")
            raise

        return self.data[scope][variable] == value

    def parse_existence(self, condition: dict) -> bool:
        try:
            scope, variable = condition["scope"].split(".")
        except (KeyError, ValueError):
            logging.error("Invalid 'scope' key for condition")
            raise

        try:
            condition_variable = condition["value"]
        except KeyError:
            logging.error("Invalid 'value' key for condition")
            raise

        variable = self.data[scope][variable]

        if variable:
            if (type(variable) is int) or (type(variable) is float):
                return condition_variable
            if type(variable) is time:
                return condition_variable == (variable > time.min)
            if type(variable) is bool:
                return condition_variable == variable
            if type(variable) is str:
                return condition_variable == (variable != "")

        return condition_variable is False

    def parse_and(self, condition: dict) -> bool:
        try:
            conditions = condition["conditions"]
        except KeyError:
            logging.error("Invalid 'conditions' key for condition")
            raise

        is_true = True

        for con in conditions:
            is_true = is_true and self.parse_condition(con, True)
            if not is_true:
                return is_true

        return is_true

    def parse_or(self, condition: dict) -> bool:
        try:
            conditions = condition["conditions"]
        except KeyError:
            logging.error("Invalid 'conditions' key for condition")
            raise

        is_true = False

        for con in conditions:
            is_true = is_true or self.parse_condition(con, True)

        return is_true

    def parse_not(self, condition: dict) -> bool:
        try:
            conditions = condition["conditions"]
        except KeyError:
            logging.error("Invalid 'conditions' key for condition")
            raise

        is_true = True

        for con in conditions:
            is_true = is_true and not self.parse_condition(con, True)

        return is_true

    def parse_data(self, dictionary: dict, data) -> str:
        result = ""

        if type(data) is not dict:
            diagnosis_dict = vars(data)
        else:
            diagnosis_dict = data

        for key, value in diagnosis_dict.items():
            if value:
                result += dictionary[key] if result == "" else f", {dictionary[key]}"

        result = self.replace_last(result, ",", " and")

        return result

    @staticmethod
    def get_tici_meaning(dictionary: dict, tici_score: str) -> str:
        if tici_score is not None and tici_score != "occlusion not confirmed":
            tici_score = int(tici_score)
            return dictionary[f"tici_score_{tici_score}"]

    @staticmethod
    def replace_last(string: str, old: str, new: str) -> str:
        return new.join(string.rsplit(old, 1))

    @staticmethod
    def translate_data(dictionary: dict, key: dict):
        if key:
            return dictionary[key]
