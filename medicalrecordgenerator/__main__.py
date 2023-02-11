import locale
import logging
import os
import sys
import getopt
from typing import Optional

import psycopg2
import psycopg2.extras
import psycopg2.extensions

from app.generator import MedicalRecordsGenerator
from app.language import Language
from utils import load_utils

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

    language_dict = load_utils.load_language(app_language)
    if not language_dict:
        return

    try:
        language = Language(**language_dict)
    except (KeyError, TypeError, AttributeError) as e:
        logging.error(repr(e))
        return

    """ Connect to the PostgreSQL database server """
    conn = None

    try:

        # connect to the PostgreSQL server
        logging.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            user=os.getenv("EMS_DB_USER"),
            password=os.getenv("EMS_DB_PASSWORD"),
            host=os.getenv("EMS_DB_HOST"),
            database=os.getenv("EMS_DB_NAME")
        )

        # create a cursor that loads data as dictionary
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Register a customized adapter for PostgreSQL to load decimal as floats
        DEC2FLOAT = psycopg2.extensions.new_type(
            psycopg2.extensions.DECIMAL.values,
            'DEC2FLOAT',
            lambda value, curs: float(value) if value is not None else None)
        psycopg2.extensions.register_type(DEC2FLOAT)

        # fetch data from database
        if subject_id:
            cur.execute("SELECT * FROM datamix WHERE subject_id=%s", subject_id)
        else:
            cur.execute("SELECT * FROM datamix")
        data = cur.fetchall()

        # generate records
        for idx, row in enumerate(data):
            generator = MedicalRecordsGenerator(language, row)
            report = generator.generate_medical_record()
            print(report)
            """
            with open(f"med_record{idx+1}.txt", "w") as file:
                file.write(report + "\n")
            """

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


if __name__ == '__main__':
    main(sys.argv[1:])
