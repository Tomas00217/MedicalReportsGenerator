import logging
from datetime import time
from typing import List, Union, Any


class Condition:
    """
    A class representing the general condition from the json file

    Methods
    -------
    parse_condition(condition)
        Parses the condition loaded from json file to the correct condition type
    parse_conditions(conditions)
        Parses the list of conditions loaded from json file to the correct list of condition types
    """

    def __init__(self, condition: dict = None):
        """

        Parameters
        ----------
        condition : dict
            Condition loaded from the json file
        """
        self.condition = self.parse_condition(condition)

    @staticmethod
    def parse_condition(condition: dict):
        """Parses the condition loaded from json file to the correct condition type

        Parameters
        ----------
        condition : dict
            Condition loaded from the json file
        Returns
        -------
        None, ConditionEmpty, ConditionValue, ConditionExistence, ConditionAnd, ConditionOr, ConditionNot
            The corresponding object with correct type of condition

        Raises
        ------
        KeyError
            When the condition is missing the 'type' key
        """

        if condition is None:
            return None

        if condition == {}:
            return ConditionEmpty()

        try:
            if condition["type"] == "VALUE":
                return ConditionValue(condition.get("scope"), condition.get("value"))
            if condition["type"] == "EXISTENCE":
                return ConditionExistence(condition.get("scope"), condition.get("value"))
            if condition["type"] == "AND":
                return ConditionAnd(condition.get("conditions"))
            if condition["type"] == "OR":
                return ConditionOr(condition.get("conditions"))
            if condition["type"] == "NOT":
                return ConditionNot(condition.get("conditions"))
        except KeyError:
            raise KeyError(f"Invalid 'type' key inside condition block")

        return ConditionEmpty()

    def parse_conditions(self, conditions: List[dict]) -> List[Any]:
        """Parses the list of conditions loaded from json file to the correct list of condition types

        Parameters
        ----------
        conditions : List[dict]
            List of conditions loaded from json file
        Returns
        -------
        List[Any]
            List with conditions with the correct type
        """
        result: List[Condition] = []
        for condition in conditions:
            result.append(self.parse_condition(condition))

        return result


class ConditionEmpty(Condition):
    """
    A class representing an empty condition

    Methods
    -------
    get_condition_result(_)
        Returns always True
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_condition_result(_) -> bool:
        """Returns always True

        Parameters
        ----------
        _

        Returns
        -------
        bool
            Always True
        """
        return True


class ConditionValue(Condition):
    """
    A class representing a VALUE condition

    Methods
    -------
    get_condition_result(dict)
        Gets the boolean result of the VALUE condition.
    """

    def __init__(self, scope: str, value: Any):
        """

        Parameters
        ----------
        scope : str
            Scope of the variable to be checked
        value : Any
            Value the variable is checked against

        Raises
        ------
        AttributeError
            If the value is missing inside the json dictionary
        """

        super().__init__()
        self.scope = scope
        self.value = value
        if value is None:
            raise TypeError("Invalid 'value' key inside condition block")

    def get_condition_result(self, data: dict) -> bool:
        """Gets the boolean result of the VALUE condition.

        Parameters
        ----------
        data : dict
            Dictionary with the values from database

        Returns
        -------
        bool
            True if the VALUE condition defined in json dictionary is true, False otherwise

        Raises
        ------
        AttributeError
            If the 'scope' or 'value' key is not defined in the condition
        ValueError
            If the scope defined is in incorrect format and cannot be split
        KeyError
            If the scope is invalid
        """

        try:
            scope, variable = self.scope.split(".")
        except (AttributeError, ValueError):
            logging.error("Invalid 'scope' key inside condition block")
            raise

        try:
            var = data[scope][variable]
        except KeyError:
            logging.error(f"Invalid key {scope}.{variable} inside condition block")
            raise

        return var == self.value


class ConditionExistence(Condition):
    """
    A class representing a EXISTENCE condition

    Methods
    -------
    get_condition_result(dict)
        Gets the boolean result of the EXISTENCE condition.
    """

    def __init__(self, scope: str, value: Any):
        """

        Parameters
        ----------
        scope : str
            Scope of the variable to be checked
        value : Any
            Value the variable is checked against

        Raises
        ------
        AttributeError
            If the value is missing inside the json dictionary
        """

        super().__init__()
        self.scope = scope
        self.value = value
        if value is None:
            raise AttributeError("Invalid 'value' key inside condition block")

    def get_condition_result(self, data: dict) -> bool:
        """Gets the boolean result of the EXISTENCE condition.

        Parameters
        ----------
        data : dict
            Dictionary with the values from database

        Returns
        -------
        bool
            True if the EXISTENCE condition defined in json dictionary is true, False otherwise

        Raises
        ------
        AttributeError
            If the 'scope' or 'value' key is not defined in the condition
        ValueError
            If the scope defined is in incorrect format and cannot be split
        KeyError
            If the scope is invalid
        """

        try:
            scope, variable = self.scope.split(".")
        except (AttributeError, ValueError):
            logging.error("Invalid 'scope' key inside condition block")
            raise

        try:
            var = data[scope][variable]
        except KeyError:
            logging.error(f"Invalid key {scope}.{variable} inside condition block")
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
    """
    A class representing an AND condition

    Methods
    -------
    get_condition_result(dict)
        Gets the boolean result of the AND condition.
    """

    def __init__(self, conditions: List[dict]):
        """

        Parameters
        ----------
        conditions : List[dict]
            List of conditions from the json file for given condition
        """

        super().__init__()
        self.conditions = self.parse_conditions(conditions)

    def get_condition_result(self, data: dict) -> bool:
        """Gets the boolean result of the OR condition.

        Parameters
        ----------
        data : dict
            Dictionary with the values from database

        Returns
        -------
        bool
            True if all conditions defined in the 'conditions' section of json dictionary are true, False otherwise
        """

        is_true = True

        for condition in self.conditions:
            is_true = is_true and condition.get_condition_result(data)
            if not is_true:
                return is_true

        return is_true


class ConditionOr(Condition):
    """
    A class representing a OR condition

    Methods
    -------
    get_condition_result(dict)
        Gets the boolean result of the OR condition.
    """

    def __init__(self, conditions: List[dict]):
        """

        Parameters
        ----------
        conditions : List[dict]
            List of conditions from the json file for given condition
        """

        super().__init__()
        self.conditions = self.parse_conditions(conditions)

    def get_condition_result(self, data: dict) -> bool:
        """Gets the boolean result of the OR condition.

        Parameters
        ----------
        data : dict
            Dictionary with the values from database

        Returns
        -------
        bool
            True if at least one condition defined in the 'conditions' section of json dictionary is true,
            False otherwise
        """

        is_true = False

        for condition in self.conditions:
            is_true = is_true or condition.get_condition_result(data)

        return is_true


class ConditionNot(Condition):
    """
    A class representing a NOT condition

    Methods
    -------
    get_condition_result(dict)
        Gets the boolean result of the NOT condition.
    """

    def __init__(self, conditions: List[dict]):
        """

        Parameters
        ----------
        conditions : List[dict]
            List of conditions from the json file for given condition
        """

        super().__init__()
        self.conditions = self.parse_conditions(conditions)

    def get_condition_result(self, data: dict) -> bool:
        """Gets the boolean result of the NOT condition.

        Parameters
        ----------
        data : dict
            Dictionary with the values from database

        Returns
        -------
        bool
            True if the negation of condition defined in the 'conditions' section of json dictionary is true,
            False otherwise
        """

        is_true = True

        for condition in self.conditions:
            is_true = is_true and not condition.get_condition_result(data)

        return is_true


class Variant:
    """
    A class representing a single variant of a block inside the json language file

    Methods
    -------
    parse_rest(kwargs)
        Parses the kwargs as either a str or MedicalRecordBlock
    get_variant_result(data)
        Gets the final result of the parsed variant
    """

    def __init__(self, condition: dict, **kwargs: dict):
        """

        Parameters
        ----------
        condition : dict
            Condition from the json file for given variant
        kwargs : dict
            Arguments passed to the variant
        """

        self.condition = Condition(condition)
        self.rest = self.parse_rest(kwargs)

    @staticmethod
    def parse_rest(kwargs: dict) -> Union[str, Any]:
        """Parses the kwargs as either a str or MedicalRecordBlock

        Parameters
        ----------
        kwargs
            Arguments passed to the variant

        Returns
        -------
        Union[str, MedicalRecordBlock]
            Text inside the variant or Nested block of data inside the variant
        """

        if "text" in kwargs.keys():
            return kwargs["text"]

        return MedicalRecordBlock(list(kwargs.keys())[0], **kwargs[list(kwargs.keys())[0]])

    def get_variant_result(self, data: dict) -> str:
        """Gets the final result of the parsed variant

        Parameters
        ----------
        data : dict
            Dictionary with the values from database

        Returns
        -------
        str
            Final text of the variant
        """

        if self.condition.condition.get_condition_result(data):
            if type(self.rest) is str:
                return self.rest

            return self.rest.get_block_result(data)

        return ""


class MedicalRecordBlock:
    """
    A class representing a block of data inside the json language file

    Methods
    -------
    parse_variants(variants)
        Parses the list of variants loaded from json to list of Variant types
    get_block_result(data)
        Gets the final result of the parsed block
    """

    def __init__(self, name: str, variants: List[dict]):
        """

        Parameters
        ----------
        name : str
            Name of the block
        variants : List[dict]
            List of variants from the json file for given block
        """

        self.name = name
        self.variants = self.parse_variants(variants)

    def parse_variants(self, variants: List[dict]) -> List[Variant]:
        """Parses the list of variants loaded from json to list of Variant types

        Parameters
        ----------
        variants : List[dict]
            List of variants from the json file for given block

        Returns
        -------
        List[Variants]
            The parsed list of variants

        Raises
        ------
        KeyError
            When the condition of one of the variants has incorrect key
        TypeError
            When an invalid block of data is present in the json file
        """

        result: List[Variant] = []
        for variant in variants:
            try:
                result.append(Variant(**variant))
            except KeyError as e:
                raise KeyError(f"{repr(e)} inside {self.name} block")
            except TypeError:
                raise TypeError(f"Missing or invalid block inside {self.name} block")

        return result

    def get_block_result(self, data: dict) -> str:
        """Gets the final result of the parsed block

        Parameters
        ----------
        data : dict
            Dictionary with the values from database

        Returns
        -------
        str
            Final text of the block
        """

        text = ""

        for variant in self.variants:
            text += variant.get_variant_result(data)

        return text


class Language:
    """
    A class representing the language loaded from the json file
    """

    def __init__(self, diagnosis: dict, onset: dict, admission: dict, treatment: dict, follow_up_imaging: dict,
                 post_acute_care: dict, post_stroke_complications: dict, etiology: dict, discharge: dict,
                 settings: dict, variables: dict):
        try:
            self.diagnosis = MedicalRecordBlock("diagnosis", **diagnosis)
            self.onset = MedicalRecordBlock("onset", **onset)
            self.admission = MedicalRecordBlock("admission", **admission)
            self.treatment = MedicalRecordBlock("treatment", **treatment)
            self.follow_up_imaging = MedicalRecordBlock("follow_up_imaging", **follow_up_imaging)
            self.post_acute_care = MedicalRecordBlock("post_acute_care", **post_acute_care)
            self.post_stroke_complications = MedicalRecordBlock("post_stroke_complications",
                                                                **post_stroke_complications)
            self.etiology = MedicalRecordBlock("etiology", **etiology)
            self.discharge = MedicalRecordBlock("discharge", **discharge)
            self.settings = settings
            self.variables = variables
        except (KeyError, TypeError, AttributeError):
            raise
