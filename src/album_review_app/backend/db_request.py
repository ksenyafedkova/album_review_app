import os
from urllib.parse import uses_relative

from dotenv import load_dotenv
import mysql.connector
from logger import logger
import streamlit as st


load_dotenv()

def _get_connection(database=None):
    kwargs = {
        "host": os.getenv('DB_HOST'),
        "user": os.getenv('DB_USER')
    }

    if database:
        kwargs['database'] = database

    return mysql.connector.connect(**kwargs)

def make_request(req, db_name, args=tuple()):
    connection = None
    cursor = None

    try:
        connection = _get_connection(db_name)
        cursor = connection.cursor(dictionary=True)

        if args:
            cursor.execute(req, args)
        else:
            cursor.execute(req)

        res = cursor.fetchall()
        return res

    except Exception as e:
        logger.error(f'Database request failed: {e}')
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

def execute_request(req, db_name, args=()):
    connection = None
    cursor = None

    try:
        connection = _get_connection(db_name)
        cursor = connection.cursor()

        if args:
            cursor.execute(req, args)
        else:
            cursor.execute(req)

        connection.commit()

    except Exception as e:
        logger.error(f'Database request failed: {e}')
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


def execute_insert(req, db_name, args=()):
    connection = None
    cursor = None

    try:
        connection = _get_connection(db_name)
        cursor = connection.cursor()

        if args:
            cursor.execute(req, args)
        else:
            cursor.execute(req)

        connection.commit()
        return cursor.lastrowid

    except Exception as e:
        logger.error(f'Database request failed: {e}')
        raise

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()
