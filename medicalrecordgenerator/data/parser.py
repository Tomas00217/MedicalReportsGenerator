from datetime import time

from medicalrecordgenerator.data.data_objects import ConditionType


def parse(dictionary, data, text=""):
    variants = dictionary["variants"]

    for variant in variants:
        condition = list(variant.values())[0]
        rest = list(variant.values())[1]
        if parse_condition(condition, True, data):
            if type(rest) is dict:
                text += parse(rest, data)
            else:
                text += rest

    return text


def parse_condition(condition, is_true, data):
    if len(condition.keys()) == 0:
        return True

    condition_type = condition["type"]

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


def parse_value(condition, data):
    scope = condition["scope"]
    value = condition["value"]

    return data[scope] == value


def parse_existence(condition, data):
    scope = condition["scope"]
    condition_variable = condition["value"]
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


def parse_and(condition, data):
    conditions = condition["conditions"]
    is_true = True

    for con in conditions:
        is_true = is_true and parse_condition(con, True, data)
        if not is_true:
            return is_true

    return is_true


def parse_or(condition, data):
    conditions = condition["conditions"]
    is_true = False

    for con in conditions:
        is_true = is_true or parse_condition(con, True, data)

    return is_true


def parse_not(condition, data):
    conditions = condition["conditions"]
    is_true = True

    for con in conditions:
        is_true = is_true and not parse_condition(con, True, data)

    return is_true


def parse_data(dictionary, data):
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


def get_tici_meaning(dictionary, tici_score):
    if tici_score is not None and tici_score != "occlusion not confirmed":
        tici_score = int(tici_score)
        return dictionary[f"tici_score_{tici_score}"]


def replace_last(string, old, new):
    return new.join(string.rsplit(old, 1))

