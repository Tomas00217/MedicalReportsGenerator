import logging
from pathlib import Path

from app.generator import MedicalReportsGenerator
from app.language import Language
from data.subject_storage import SubjectStorage
from utils.definitions import DEFAULT_CSV_PATH, DEFAULT_TEMPLATE_PATH
from utils.load_language_utils import load_language
from typing import Optional


def generate(app_language: str, subject_id: Optional[int], load_csv: Optional[bool] = False,
             csv_file: Optional[str] = DEFAULT_CSV_PATH,
             definition_template_path: Optional[Path] = DEFAULT_TEMPLATE_PATH) -> str:
    """Generates all medical records for each row in the postgres database if the subject_id is None.
    Otherwise, generates only one medical record for the specified subject.

    Parameters
    ----------
    app_language : str
        The language of the medical record to be generated in
    subject_id : Optional[int]
        The id of subject for which the medical record should be generated. If none, all subjects are generated.
    load_csv : Optional[bool]
        Boolean value deciding whether we load the data from csv or not
    csv_file : Optional[str]
        Path to csv file
    definition_template_path : Optional[Path]
        Path to file with the template

    Returns
    -------
    str
        Returns the generated reports
    """
    report = ""

    subject_storage = SubjectStorage(load_csv, csv_file)
    data = subject_storage.get_data(subject_id)

    if data:
        # load language
        language_dict = load_language(app_language)
        if not language_dict:
            return ""

        try:
            language = Language(**language_dict)
        except (KeyError, TypeError, AttributeError) as e:
            logging.error(repr(e))
            return ""

        # generate records
        for idx, row in enumerate(data):
            generator = MedicalReportsGenerator(language, row)
            report += generator.generate_medical_report(definition_template_path) + "\n"
    else:
        logging.info("No data found")

    return report


def list_ids(load_csv: bool, csv_file: str):
    subject_storage = SubjectStorage(load_csv, csv_file)
    data = subject_storage.get_subject_ids()

    return data
