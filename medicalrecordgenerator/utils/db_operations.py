import logging
import os
from typing import Optional, Any

import psycopg2
import psycopg2.extras
import psycopg2.extensions

from utils.queries import select_all, select_by_id


def get_patient_info(subject_id: Optional[int] = None) -> list[tuple[Any, ...]]:
    """Creates connection to the database and fetches data about patient

    Parameters
    ----------
    subject_id
        The id of subject for which the medical record should be generated.

    Returns
    -------
        Fetched data from database
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

        # Register a customized adapter for PostgreSQL to load decimal as floats
        DEC2FLOAT = psycopg2.extensions.new_type(
            psycopg2.extensions.DECIMAL.values,
            'DEC2FLOAT',
            lambda value, curs: float(value) if value is not None else None)
        psycopg2.extensions.register_type(DEC2FLOAT)

        data = get_patient_info_from_db(conn, subject_id)

        return data
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')


def get_patient_info_from_db(conn, subject_id: Optional[int] = None) -> list[tuple[Any, ...]]:
    """Fetches data about patient from the database

    Parameters
    ----------
    conn
        Connection to the database from which we create the cursor
    subject_id
        The id of subject for which the medical record should be generated.

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
