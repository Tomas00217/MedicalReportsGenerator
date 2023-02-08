import logging

from datetime import time

from data.data_objects import ConditionType


class Parser:
    """
    A class representing custom parser used to parse dictionary in json format.

    ...

    Methods
    -------
    parse(data)
        Recursively parses the whole document
    parse_condition(condition, is_true)
        Parses the condition block from dictionary passed to the function
    parse_value(condition)
        Parses the VALUE type of condition
    parse_existence(condition)
        Parses the EXISTENCE type of condition
    parse_and(condition)
        Parses the AND type of condition
    parse_or(condition)
        Parses the OR type of condition
    parse_not(condition)
        Parses the NOT type of condition
    parse_data(dictionary, data)
        Parses the variables from dictionary specified by the data
    translate_data(dictionary, key)
        Translates the data specified by key with the values from dictionary
    get_tici_meaning(dictionary, tici_score)
        Gets the tici meaning based on the tici score
    replace_last(string, old, new)
        Replaces the last substring with new substring of given string

    """

    def __init__(self, data: dict):
        """
        Parameters
        ----------
        data : dict
            All the data used for parsing.
        """
        self.data = data

    def parse(self, dictionary: dict) -> str:
        """Recursively parses the whole document

        If KeyError occurs during parsing, returns empty string

        Parameters
        ----------
        dictionary : dict
            Part of the json dictionary to be parsed

        Returns
        -------
        str
            Text from the json dictionary acquired by parsing the dictionary
        """

        text = ""

        try:
            variants = dictionary["variants"]
        except KeyError:
            logging.error("Invalid key, try 'variants'")
            return text

        for variant in variants:
            condition = list(variant.values())[0]
            rest = list(variant.values())[1]
            if self.parse_condition(condition):
                if type(rest) is dict:
                    text += self.parse(rest)
                else:
                    text += rest

        return text

    def parse_condition(self, condition: dict) -> bool:
        """Parses the condition block from dictionary passed to the function

        Parameters
        ----------
        condition : dict
            The condition that is being parsed

        Returns
        -------
        bool
            True if the condition defined in json dictionary is true, False otherwise

        Raises
        ------
        KeyError
            If the 'type' key is not defined in the condition
        """

        is_true = True

        if len(condition.keys()) == 0:
            return True

        try:
            condition_type = condition["type"]
        except KeyError:
            logging.error("Invalid condition key for %s, try 'type'", condition)
            raise

        if condition_type == ConditionType.Value.value:
            is_true = self.parse_value(condition)
        elif condition_type == ConditionType.Existence.value:
            is_true = self.parse_existence(condition)
        elif condition_type == ConditionType.And.value:
            is_true = self.parse_and(condition)
        elif condition_type == ConditionType.Or.value:
            is_true = self.parse_or(condition)
        elif condition_type == ConditionType.Not.value:
            is_true = self.parse_not(condition)

        return is_true

    def parse_value(self, condition: dict) -> bool:
        """Parses the VALUE type of condition

        Parameters
        ----------
        condition : dict
            The condition of type VALUE that is being parsed

        Returns
        -------
        bool
            True if the VALUE condition defined in json dictionary is true, False otherwise

        Raises
        ------
        KeyError
            If the 'scope' or 'value' key is not defined in the condition
        ValueError
            If the scope defined is in incorrect format and cannot be split
        """

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
        """Parses the EXISTENCE type of condition

        Parameters
        ----------
        condition : dict
            The condition of type EXISTENCE that is being parsed

        Returns
        -------
        bool
            True if the EXISTENCE condition defined in json dictionary is true, False otherwise

        Raises
        ------
        KeyError
            If the 'scope' or 'value' key is not defined in the condition
        ValueError
            If the scope defined is in incorrect format and cannot be split
        """

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
        """Parses the AND type of condition

        Parameters
        ----------
        condition : dict
            The condition of type AND that is being parsed

        Returns
        -------
        bool
            True if all conditions defined in the 'conditions' section of json dictionary are true, False otherwise

        Raises
        ------
        KeyError
            If the 'conditions' key is not defined in the condition
        """

        try:
            conditions = condition["conditions"]
        except KeyError:
            logging.error("Invalid 'conditions' key for condition")
            raise

        is_true = True

        for con in conditions:
            is_true = is_true and self.parse_condition(con)
            if not is_true:
                return is_true

        return is_true

    def parse_or(self, condition: dict) -> bool:
        """Parses the OR type of condition

        Parameters
        ----------
        condition : dict
            The condition of type OR that is being parsed

        Returns
        -------
        bool
            True if at least one condition defined in the 'conditions' section of json dictionary is true,
            False otherwise

        Raises
        ------
        KeyError
            If the 'conditions' key is not defined in the condition
        """

        try:
            conditions = condition["conditions"]
        except KeyError:
            logging.error("Invalid 'conditions' key for condition")
            raise

        is_true = False

        for con in conditions:
            is_true = is_true or self.parse_condition(con)

        return is_true

    def parse_not(self, condition: dict) -> bool:
        """Parses the NOT type of condition

        Parameters
        ----------
        condition : dict
            The condition of type NOT that is being parsed

        Returns
        -------
        bool
            True if the negation of condition defined in the 'conditions' section of json dictionary is true,
            False otherwise

        Raises
        ------
        KeyError
            If the 'conditions' key is not defined in the condition
        """

        try:
            conditions = condition["conditions"]
        except KeyError:
            logging.error("Invalid 'conditions' key for condition")
            raise

        is_true = True

        for con in conditions:
            is_true = is_true and not self.parse_condition(con)

        return is_true

    def parse_data(self, dictionary: dict, data: dict) -> str:
        """Parses the variables from dictionary specified by the data

        Parameters
        ----------
        dictionary : dict
            A dictionary from which the text versions are taken from
        data : dict
            A dictionary with the data to be parsed

        Returns
        -------
        str
            The resulting parsed text from json dictionary based on the data
        """

        result = ""
        if dictionary is None:
            return result

        for key, value in data.items():
            if value:
                variable = ""

                try:
                    variable = dictionary[key]
                except KeyError:
                    logging.error("Invalid key %s", key)

                result += variable if result == "" else f", {variable}"

        result = self.replace_last(result, ",", " and")

        return result

    @staticmethod
    def translate_data(dictionary: dict, key: str) -> str:
        """Translates the data specified by key with the values from dictionary

        Parameters
        ----------
        dictionary : dict
            Dictionary used for the translation
        key : str
            The key for the value from data dictionary that is to be translated

        Returns
        -------
        str
            Translated value
        """

        if dictionary is None:
            return ""

        if key:
            try:
                variable = dictionary[key]
            except KeyError:
                logging.error("Invalid key %s", key)
                variable = ""

            return variable

        return ""

    @staticmethod
    def get_tici_meaning(dictionary: dict, tici_score: str) -> str:
        """Gets the tici meaning based on the tici score

        Parameters
        ----------
        dictionary : dict
            Dictionary from which the text is being taken
        tici_score : str
            Tici score of patient

        Returns
        -------
        str
            Parsed tici meaning based on the tici score

        """

        if dictionary is None:
            return ""

        if tici_score is not None and tici_score != "occlusion not confirmed":
            tici_score = tici_score
            return dictionary[f"tici_score_{tici_score}"]

    @staticmethod
    def replace_last(string: str, old: str, new: str) -> str:
        """Replaces the last substring with new substring of given string

        Parameters
        ----------
        string : str
            The string in which we are replacing substrings
        old : str
            The last occurrence of the string to be replaced
        new : str
            The replacement string

        Returns
        -------
        str
            The replaced string
        """

        return new.join(string.rsplit(old, 1))
