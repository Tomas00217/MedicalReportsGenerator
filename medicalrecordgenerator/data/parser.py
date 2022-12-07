import json
from datetime import time


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
    for con in condition:
        if con == "AND":
            is_true = is_true and parse_and(condition[con], True, data)
        elif con == "OR":
            is_true = is_true and parse_or(condition[con], False, data)
        else:
            is_true = is_true and parse_con(condition, data)

    return is_true


def parse_and(condition, is_true, data):
    for con in condition:
        key = list(con.keys())[0]
        if key == "AND":
            is_true = is_true and parse_and(con[key], True, data)
        elif key == "OR":
            is_true = is_true and parse_or(con[key], False, data)
        else:
            is_true = is_true and parse_con(con, data)

        if not is_true:
            return False

    return True


def parse_or(condition, is_true, data):
    for con in condition:
        key = list(con.keys())[0]
        if key == "AND":
            is_true = is_true or parse_and(con[key], True, data)
        elif key == "OR":
            is_true = is_true or parse_or(con[key], False, data)
        else:
            is_true = is_true or parse_con(con, data)

    return is_true


def parse_con(condition, data):
    key = list(condition.keys())[0]
    condition_variable = condition[key]
    variable = data[key]

    if type(condition_variable) is bool:
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

    return condition_variable == variable


def parse_data(dictionary, data):
    result = ""

    if type(data) is not dict:
        diagnosis_dict = vars(data)
    else:
        diagnosis_dict = data

    for key, value in diagnosis_dict.items():
        if value:
            result += dictionary[key] if result == "" else f", {dictionary[key]}"

    return result
