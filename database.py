import mysql.connector
from config import DB_CONFIG


class Database:
    """Creates MySQL connections for the application."""

    def get_connection(self):
        return mysql.connector.connect(**DB_CONFIG)
