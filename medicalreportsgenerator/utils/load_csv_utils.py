import numpy as np
import pandas as pd
from typing import Optional

from utils.definitions import DEFAULT_CSV_PATH


def load_data_from_csv_file(subject_id: Optional[int], csv_file: str = DEFAULT_CSV_PATH):
    """Loads data from csv file

    Returns
    -------
    dict
        Dictionary with key value pairs of data from csv

    """
    df = pd.read_csv(csv_file)
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

    if subject_id is not None:
        try:
            return [data[int(subject_id) - 1]]
        except IndexError:
            raise IndexError("Invalid subject id, try running with option --list to list available ids")

    return data


def load_ids_from_csv_file(csv_file: str = DEFAULT_CSV_PATH):
    df = pd.read_csv(csv_file, usecols=['subject_id'])

    ids = sorted(df['subject_id'].values.tolist())

    return ids
