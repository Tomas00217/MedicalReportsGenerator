import locale
import logging
import sys
import getopt

import psycopg2
import psycopg2.extras

from app.generator import MedicalRecordsGenerator
from medicalrecordgenerator.config import config
from utils import load_utils

OPTIONS = "l:"
LONG_OPTIONS = ["language="]


def main(argv=None):
    app_language = 'en_US'

    try:
        opts, args = getopt.getopt(argv, OPTIONS, LONG_OPTIONS)
        for opt, arg in opts:
            if opt in "-l, --language":
                app_language = arg
    except getopt.GetoptError as err:
        print(err)

    generate(app_language)


def generate(app_language: str) -> None:
    locale.setlocale(locale.LC_ALL, app_language)

    language = load_utils.load_language(app_language)

    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        logging.info('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # fetch data from database
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
