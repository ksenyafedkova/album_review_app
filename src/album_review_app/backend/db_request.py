import os

from dotenv import load_dotenv
import mysql.connector
from logger import logger

load_dotenv()

def _get_connection(database=None):
    kwargs = {
        "host": os.getenv('DB_HOST'),
        "user": os.getenv('DB_USER')
    }

    if database:
        kwargs['database'] = database

    return mysql.connector.connect(**kwargs)


class DatabaseClient:

    def __init__(self, database):
        self.database = database
        self.connection = None

    def __enter__(self):
        self.connection = _get_connection(self.database)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if self.connection:
                if exc_type is not None:
                    self.connection.rollback()
        finally:
            if self.connection:
                self.connection.close()
                self.connection = None

        return False

    def _execute(self, req, args=(), dictionary=False):
        cursor = None

        try:
            cursor = self.connection.cursor(dictionary=dictionary)
            cursor.execute(req, args)
            return cursor

        except Exception as e:
            if cursor:
                cursor.close()
            logger.error(f"Database request failed: {e}")
            raise

    def make_request(self, req, args=()):
        cursor = None

        try:
            cursor = self._execute(req, args, dictionary=True)
            return cursor.fetchall()

        finally:
            if cursor:
                cursor.close()

    def execute_request(self, req, args=()):
        cursor = None

        try:
            cursor = self._execute(req, args)
            self.connection.commit()

        except Exception:
            self.connection.rollback()
            raise

        finally:
            if cursor:
                cursor.close()

    def execute_insert(self, req, args=()):
        cursor = None

        try:
            cursor = self._execute(req, args)
            lastrowid = cursor.lastrowid
            self.connection.commit()
            return lastrowid

        except Exception:
            self.connection.rollback()
            raise

        finally:
            if cursor:
                cursor.close()