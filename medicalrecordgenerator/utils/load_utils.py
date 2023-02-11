import json
import glob
import logging

import numpy as np
import pandas as pd


DEFAULT_LANGUAGE = 'locales\\en_US.json'
PATH = '..\\locales\\*.json'


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
    language_list = glob.glob(PATH)

    for lang in language_list:
        filename = lang.split('\\')
        lang_code = filename[-1].split('.')[0]

        if lang_code == app_language:
            return load_language_file(lang)

    return load_language_file(DEFAULT_LANGUAGE)


def load_language_file(file_name: str) -> dict:
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
