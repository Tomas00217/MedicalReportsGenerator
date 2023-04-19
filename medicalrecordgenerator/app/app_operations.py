import logging

from app.generator import MedicalRecordsGenerator
from app.language import Language
from utils import load_utils
from utils.db_operations import get_patient_info
from utils.load_utils import load_csv_file
from typing import Optional

TEMPLATES_PATH = "templates"
DEFAULT_TEMPLATE = "main.txt"


def generate(app_language: str, load_csv: bool, subject_id: Optional[int] = None) -> None:
    """Generates all medical records for each row in the postgres database if the subject_id is None.
    Otherwise, generates only one medical record for the specified subject.

    Parameters
    ----------
    app_language : str
        The language of the medical record to be generated in
    load_csv
        Boolean value deciding whether we load the data from csv or not
    subject_id : Optional[int]
        The id of subject for which the medical record should be generated.

    Returns
    -------
    None
        Doesn't return nothing yet, just prints the result
    """

    if load_csv:
        data = load_csv_file(subject_id)
    else:
        data = get_patient_info(subject_id)

    if data:
        # load language
        language_dict = load_utils.load_language(app_language)
        if not language_dict:
            return

        try:
            language = Language(**language_dict)
        except (KeyError, TypeError, AttributeError) as e:
            logging.error(repr(e))
            return

        # generate records
        for idx, row in enumerate(data):
            generator = MedicalRecordsGenerator(language, row)
            report = generator.generate_medical_record(TEMPLATES_PATH, DEFAULT_TEMPLATE)
            print(report)
            """
            with open(f"med_record{idx+1}.txt", "w") as file:
                file.write(report + "\n")
            """


def show_help():
    help_str = f"Medical Reports Generator\n" \
               f"-h, --help -> Shows the help screen\n" \
               f"-i, --subject_id -> Specifies the id of the subject for which we want to generate the report. " \
               f"None by default, resulting in generating for every subject.\n" \
               f"-l, --language -> Specifies the language file which we want to use for the generation process. " \
               f"en_US by default.\n" \
               f"--csv -> Option for test and showcase purposes reading from the csv instead of database."
    print(help_str)
