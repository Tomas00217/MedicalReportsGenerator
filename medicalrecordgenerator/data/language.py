import logging
from datetime import time
from typing import List, Union, Any


class Condition:
    def __init__(self, condition: dict = None):
        self.condition = self.parse_condition(condition)

    @staticmethod
    def parse_condition(condition: dict):
        if condition is None:
            return None

        if condition.get("type") == "VALUE":
            return ConditionValue(condition.get("scope"), condition.get("value"))
        if condition.get("type") == "EXISTENCE":
            return ConditionExistence(condition.get("scope"), condition.get("value"))
        if condition.get("type") == "AND":
            return ConditionAnd(condition.get("conditions"))
        if condition.get("type") == "OR":
            return ConditionOr(condition.get("conditions"))
        if condition.get("type") == "NOT":
            return ConditionNot(condition.get("conditions"))
        return ConditionEmpty()

    def parse_conditions(self, conditions: List[dict]) -> List[Any]:
        result: List[Condition] = []
        for condition in conditions:
            result.append(self.parse_condition(condition))

        return result


class ConditionEmpty(Condition):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_condition_result(_) -> bool:
        return True


class ConditionValue(Condition):
    def __init__(self, scope: str, value: Any):
        super().__init__()
        self.scope = scope
        self.value = value

    def get_condition_result(self, data: dict) -> bool:
        try:
            scope, variable = self.scope.split(".")
        except ValueError:
            logging.error("Invalid 'scope' for condition")
            raise

        return data[scope][variable] == self.value


class ConditionExistence(Condition):
    def __init__(self, scope: str, value: Any):
        super().__init__()
        self.scope = scope
        self.value = value

    def get_condition_result(self, data: dict) -> bool:
        try:
            scope, variable = self.scope.split(".")
        except ValueError:
            logging.error("Invalid 'scope' for condition")
            raise

        try:
            var = data[scope][variable]
        except KeyError:
            logging.error(f"Invalid key {scope}.{variable}")
            raise

        if var:
            if (type(var) is int) or (type(var) is float):
                return self.value
            if type(var) is time:
                return self.value == (var > time.min)
            if type(var) is bool:
                return self.value == var
            if type(var) is str:
                return self.value == (var != "")

        return self.value is False


class ConditionAnd(Condition):
    def __init__(self, conditions: List[dict]):
        super().__init__()
        self.conditions = self.parse_conditions(conditions)

    def get_condition_result(self, data: dict) -> bool:
        is_true = True

        for condition in self.conditions:
            is_true = is_true and condition.get_condition_result(data)
            if not is_true:
                return is_true

        return is_true


class ConditionOr(Condition):
    def __init__(self, conditions: List[dict]):
        super().__init__()
        self.conditions = self.parse_conditions(conditions)

    def get_condition_result(self, data: dict) -> bool:
        is_true = False

        for condition in self.conditions:
            is_true = is_true or condition.get_condition_result(data)

        return is_true


class ConditionNot(Condition):
    def __init__(self, conditions: List[dict]):
        super().__init__()
        self.conditions = self.parse_conditions(conditions)

    def get_condition_result(self, data: dict) -> bool:
        is_true = False

        for condition in self.conditions:
            is_true = is_true and not condition.get_condition_result(data)

        return is_true


class Variant:
    def __init__(self, condition: dict, **kwargs):
        self.condition = Condition(condition)
        self.rest = self.parse_rest(kwargs)

    @staticmethod
    def parse_rest(kwargs: dict) -> Union[str, Any]:
        if "text" in kwargs.keys():
            return kwargs["text"]

        return MedicalRecordBlock(**kwargs[list(kwargs.keys())[0]])

    def get_variant_result(self, data: dict) -> str:
        if self.condition.condition.get_condition_result(data):
            if type(self.rest) is str:
                return self.rest

            return self.rest.get_block_result(data)

        return ""


class MedicalRecordBlock:
    def __init__(self, variants: List[dict]):
        self.variants = self.parse_variants(variants)

    @staticmethod
    def parse_variants(variants: List[dict]) -> List[Variant]:
        result: List[Variant] = []
        for variant in variants:
            result.append(Variant(**variant))

        return result

    def get_block_result(self, data: dict) -> str:
        text = ""

        for variant in self.variants:
            text += variant.get_variant_result(data)

        return text


class Language:
    def __init__(self, diagnosis: dict, onset: dict, admission: dict, treatment: dict, follow_up_imaging: dict,
                 post_acute_care: dict, post_stroke_complications: dict, etiology: dict, discharge: dict,
                 settings: dict, variables: dict):
        self.diagnosis = MedicalRecordBlock(**diagnosis)
        self.onset = MedicalRecordBlock(**onset)
        self.admission = MedicalRecordBlock(**admission)
        self.treatment = MedicalRecordBlock(**treatment)
        self.follow_up_imaging = MedicalRecordBlock(**follow_up_imaging)
        self.post_acute_care = MedicalRecordBlock(**post_acute_care)
        self.post_stroke_complications = MedicalRecordBlock(**post_stroke_complications)
        self.etiology = MedicalRecordBlock(**etiology)
        self.discharge = MedicalRecordBlock(**discharge)
        self.settings = settings
        self.variables = variables
