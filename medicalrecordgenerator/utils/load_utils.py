import json
import glob
import logging

import numpy as np
import pandas as pd


DEFAULT_LANGUAGE = 'locales\\en_US.json'
PATH = 'locales\\*.json'


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
            return load_json_file(lang)

    return load_json_file(DEFAULT_LANGUAGE)


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


def load_csv_file():
    """Loads data from csv file

    Returns
    -------
    dict
        Dictionary with key value pairs of data from csv

    """
    df = pd.read_csv("data\\data.csv")
    df = df.replace({"f": False})
    df = df.replace({"t": True})

    # Pandas mark column as float if at least one record contains NaN, therefore manual conversion to int is necessary
    df = df.astype({"post_treatment_imaging_id": 'Int64',
                    "smoking_cessation_id": 'Int64',
                    "speech_therapy_done_id": 'Int64',
                    "stroke_management_appointment_id": 'Int64',
                    "stroke_mimics_diagnosis_id": 'Int64',
                    "swallowing_assessment_by_id": 'Int64',
                    "swallowing_screening_type_id": 'Int64',
                    "aspects_score": 'Int64',
                    "prestroke_mrs": 'Int64',
                    "discharge_date": "datetime64[ns]",
                    "contact_date": "datetime64[ns]",
                    "discharge_mrs": 'Int64',
                    "discharge_nihss_score": 'Int64',
                    "door_to_needle": 'Int64',
                    "door_to_groin": 'Int64',
                    "door_to_door": 'Int64',
                    "ivt_dose": 'Int64',
                    })
    df = df.replace({np.nan: None})
    data = df.to_dict("records")
    return data
