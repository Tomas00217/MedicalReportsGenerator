import json
import glob
import numpy as np
import pandas as pd
from collections import namedtuple


DEFAULT_LANGUAGE = 'locales\\en_US.json'
PATH = 'locales\\*.json'


def load_xlsx(file_path):
    df = pd.read_excel(file_path)
    df = df.replace({np.nan: None})

    return df


def load_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.replace({np.nan: None})

    data = df.to_dict("records")

    return data


def load_language(app_language):
    language_list = glob.glob(PATH)

    for lang in language_list:
        filename = lang.split('\\')
        lang_code = filename[-1].split('.')[0]

        if lang_code == app_language:
            return load_language_file(lang)

    return load_language_file(DEFAULT_LANGUAGE)


def load_language_file(file_name):
    with open(file_name, 'r', encoding='utf8') as file:
        language = json.loads(file.read())

        return language
