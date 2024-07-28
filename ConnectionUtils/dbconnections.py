import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from decimal import Decimal
from datetime import datetime

class PostgresConnection(object):
    """
    PostgresConnection class to manage PostgreSQL connections and operations.
    """

    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """
        Establish a connection to the PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            self.close()

    def close(self):
        """
        Close the database connection and cursor.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def reconnect_db(self):
        """
        Reconnect to the database if the connection is lost.
        """
        self.close()
        self.connect()

    @staticmethod
    def parsed_db_result(db_data) -> dict:
        """
        Parse the database results to handle specific data types.
        """
        parsed_db_data = dict()
        for key, val in db_data.items():
            if isinstance(val, Decimal):
                parsed_db_data[key] = float(val)
            elif isinstance(val, datetime):
                parsed_db_data[key] = val.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(val, str) and val == 'NULL':
                parsed_db_data[key] = None
            else:
                parsed_db_data[key] = val
        return parsed_db_data

    def query_db(self, query, params=None) -> list:
        """
        Execute a query and return all results.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall()
            return [self.parsed_db_result(row) for row in result] if result else []
        except Exception as e:
            print(f"Query failed: {e}")
            self.reconnect_db()
            return []

    def query_db_one(self, query, params=None, parsed=True) -> dict:
        """
        Execute a query and return a single result.
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchone()
            return self.parsed_db_result(result) if result and parsed else result
        except Exception as e:
            print(f"Query failed: {e}")
            self.reconnect_db()
            return {}

    def write_db(self, query, params=None) -> int:
        """
        Execute a write operation (INSERT, UPDATE, DELETE).
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.lastrowid if self.cursor.lastrowid else 0
        except Exception as e:
            print(f"Write operation failed: {e}")
            self.reconnect_db()
            return 0


