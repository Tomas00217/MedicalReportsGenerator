import logging
import os
from typing import Optional, Any

import psycopg2
import psycopg2.extras
import psycopg2.extensions


def get_patient_info(subject_id: Optional[int] = None) -> list[tuple[Any, ...]]:
    """Gets the patient info from database.

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
            cur.execute("SELECT * FROM strokehealthcaremodel_strokehealthcaremodel WHERE subject_id=%s", subject_id)
        else:
            cur.execute("SELECT * FROM strokehealthcaremodel_strokehealthcaremodel")
        data = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()

        return data
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Database connection closed.')
