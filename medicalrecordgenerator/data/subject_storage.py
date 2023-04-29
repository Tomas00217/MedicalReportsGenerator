import logging
import os
from typing import Optional, Any

import psycopg2
import psycopg2.extras
import psycopg2.extensions

from utils.definitions import DEFAULT_CSV_PATH
from utils.load_csv_utils import load_ids_from_csv_file, load_data_from_csv_file
from utils.queries import select_all, select_by_id, select_subject_ids


class SubjectStorage:
    def __init__(self, from_csv: bool = False, csv_file: str = DEFAULT_CSV_PATH):
        self.from_csv = from_csv
        self.csv_file = csv_file

    def get_data(self, subject_id: Optional[int] = None):
        if self.from_csv:
            return load_data_from_csv_file(subject_id, self.csv_file)

        return self.get_patient_info(False, subject_id)

    def get_subject_ids(self):
        if self.from_csv:
            return load_ids_from_csv_file(self.csv_file)

        return self.get_patient_info(True, None)

    def get_patient_info(self, only_ids: bool = False, subject_id: Optional[int] = None) -> Any:
        """Creates a connection to the database and fetches data about patients, which can be either only the ids,
        or all the data

        Parameters
        ----------
        only_ids : bool
            Boolean deciding whether to return only ids or all data about patients/patient
        subject_id : int
            The id of the subject for which the medical report should be generated.

        Returns
        -------
            Fetched data from the database
        """

        # Connect to the PostgreSQL database server
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

            # Register a customized adapter for PostgreSQL to load decimals as floats
            DEC2FLOAT = psycopg2.extensions.new_type(
                psycopg2.extensions.DECIMAL.values,
                'DEC2FLOAT',
                lambda value, curs: float(value) if value is not None else None)
            psycopg2.extensions.register_type(DEC2FLOAT)

            if only_ids:
                return self.get_patient_ids_from_db(conn)

            return self.get_patient_info_from_db(conn, subject_id)
        except (Exception, psycopg2.DatabaseError) as error:
            raise psycopg2.DatabaseError(f"{error} Have you set up the environment variables for database correctly?")
        finally:
            if conn is not None:
                conn.close()
                logging.info('Database connection closed.')

    @staticmethod
    def get_patient_info_from_db(conn, subject_id: Optional[int] = None) -> list[tuple[Any, ...]]:
        """Fetches data about patient from the database

        Parameters
        ----------
        conn
            Connection to the database from which we create the cursor
        subject_id
            The id of subject for which the medical report should be generated.

        Returns
        -------
            Fetched data from database
        """

        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            # fetch data from database
            if subject_id:
                select = select_by_id(subject_id)
                cursor.execute(select, subject_id)
            else:
                select = select_all(True)
                cursor.execute(select)
            data = cursor.fetchall()

        return data

    @staticmethod
    def get_patient_ids_from_db(conn) -> list[int]:
        """Fetches subject ids from the database

        Parameters
        ----------
        conn
            Connection to the database from which we create the cursor

        Returns
        -------
            Fetched subject ids from database
        """

        with conn.cursor() as cursor:
            select = select_subject_ids()
            cursor.execute(select)

            data = cursor.fetchall()

        return [r[0] for r in data]
