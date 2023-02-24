import locale
import logging
import sys
import getopt
from typing import Optional



from app.generator import MedicalRecordsGenerator
from app.language import Language
from utils import load_utils
from utils.db_operations import get_patient_info

OPTIONS = "l:i:"
LONG_OPTIONS = ["language=", "subject_id="]


def main(argv=None):
    app_language = 'en_US'
    subject_id = None

    try:
        opts, args = getopt.getopt(argv, OPTIONS, LONG_OPTIONS)
        for opt, arg in opts:
            if opt in "-l, --language":
                app_language = arg
            if opt in "-i, --subject_id":
                subject_id = arg
    except getopt.GetoptError as err:
        logging.error(err)

    generate(app_language, subject_id)


def generate(app_language: str, subject_id: Optional[int] = None) -> None:
    """Generates all medical records for each row in the postgres database if the subject_id is None.
    Otherwise, generates only one medical record for the specified subject.

    Parameters
    ----------
    app_language : str
        The language of the medical record to be generated in
    subject_id : Optional[int]
        The id of subject for which the medical record should be generated.

    Returns
    -------
    None
        Doesn't return nothing yet, just prints the result
    """

    locale.setlocale(locale.LC_ALL, app_language)

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
            report = generator.generate_medical_record()
            print(report)
            """
            with open(f"med_record{idx+1}.txt", "w") as file:
                file.write(report + "\n")
            """


if __name__ == '__main__':
    main(sys.argv[1:])
