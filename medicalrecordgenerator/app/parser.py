import logging

from datetime import time

from medicalrecordgenerator.data.data_objects import ConditionType


def parse(dictionary: dict, data: dict, text: str = "") -> str:
    try:
        variants = dictionary["variants"]
    except KeyError:
        logging.error("Invalid key, try 'variants'")
        return text

    for variant in variants:
        condition = list(variant.values())[0]
        rest = list(variant.values())[1]
        if parse_condition(condition, True, data):
            if type(rest) is dict:
                text += parse(rest, data)
            else:
                text += rest

    return text


def parse_condition(condition: dict, is_true: bool, data: dict) -> bool:
    if len(condition.keys()) == 0:
        return True

    try:
        condition_type = condition["type"]
    except KeyError:
        logging.error("Invalid condition key for %s, try 'type'", condition)
        raise

    if condition_type == ConditionType.Value.value:
        is_true = is_true and parse_value(condition, data)
    elif condition_type == ConditionType.Existence.value:
        is_true = is_true and parse_existence(condition, data)
    elif condition_type == ConditionType.And.value:
        is_true = is_true and parse_and(condition, data)
    elif condition_type == ConditionType.Or.value:
        is_true = is_true and parse_or(condition, data)
    elif condition_type == ConditionType.Not.value:
        is_true = is_true and parse_not(condition, data)

    return is_true


def parse_value(condition: dict, data: dict) -> bool:
    try:
        scope = condition["scope"]
    except KeyError:
        logging.error("Invalid 'scope' key for condition")
        raise

    try:
        value = condition["value"]
    except KeyError:
        logging.error("Invalid 'value' key for condition")
        raise

    return data[scope] == value


def parse_existence(condition: dict, data: dict) -> bool:
    try:
        scope = condition["scope"]
    except KeyError:
        logging.error("Invalid 'scope' key for condition")
        raise

    try:
        condition_variable = condition["value"]
    except KeyError:
        logging.error("Invalid 'value' key for condition")
        raise

    variable = data[scope]

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


def parse_and(condition: dict, data: dict) -> bool:
    try:
        conditions = condition["conditions"]
    except KeyError:
        logging.error("Invalid 'conditions' key for condition")
        raise

    is_true = True

    for con in conditions:
        is_true = is_true and parse_condition(con, True, data)
        if not is_true:
            return is_true

    return is_true


def parse_or(condition: dict, data: dict) -> bool:
    try:
        conditions = condition["conditions"]
    except KeyError:
        logging.error("Invalid 'conditions' key for condition")
        raise

    is_true = False

    for con in conditions:
        is_true = is_true or parse_condition(con, True, data)

    return is_true


def parse_not(condition: dict, data: dict) -> bool:
    try:
        conditions = condition["conditions"]
    except KeyError:
        logging.error("Invalid 'conditions' key for condition")
        raise

    is_true = True

    for con in conditions:
        is_true = is_true and not parse_condition(con, True, data)

    return is_true


def parse_data(dictionary: dict, data: dict) -> str:
    result = ""

    if type(data) is not dict:
        diagnosis_dict = vars(data)
    else:
        diagnosis_dict = data

    for key, value in diagnosis_dict.items():
        if value:
            result += dictionary[key] if result == "" else f", {dictionary[key]}"

    result = replace_last(result, ",", " and")

    return result


def get_tici_meaning(dictionary: dict, tici_score: str) -> str:
    if tici_score is not None and tici_score != "occlusion not confirmed":
        tici_score = int(tici_score)
        return dictionary[f"tici_score_{tici_score}"]


def replace_last(string: str, old: str, new: str) -> str:
    return new.join(string.rsplit(old, 1))


def translate_data(dictionary: dict, key: dict):
    if key:
        return dictionary[key]

