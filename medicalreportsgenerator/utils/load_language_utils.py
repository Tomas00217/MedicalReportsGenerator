import json
import logging
from utils.definitions import LOCALE_PATH, DEFAULT_LOCALE


def load_language(app_language: str) -> dict:
    """Loads the language dictionary for given language

    Parameters
    ----------
    app_language : str
        Language for which the dictionary should be loaded

    Returns
    -------
    dict
        Dictionary for the given language

    """
    language_list = LOCALE_PATH.glob("*.json")

    for lang in language_list:
        lang_code = lang.stem
        if lang_code == app_language:
            return load_json_file(lang)

    return load_json_file(DEFAULT_LOCALE)


def load_json_file(file_name: str) -> dict:
    """Loads the json file

    Parameters
    ----------
    file_name : str
        Name of the json file to be loaded

    Returns
    -------
    dict
        Dictionary from the loaded json file

    """
    with open(file_name, 'r', encoding='utf8') as file:
        language = {}
        try:
            language = json.loads(file.read())
        except json.decoder.JSONDecodeError as e:
            logging.error(e)

        return language
