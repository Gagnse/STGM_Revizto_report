import os
import mysql.connector
from mysql.connector import Error


def get_db_connection():
    """
    Create a database connection to MySQL
    Returns connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', 'sebas1234'),
            port=os.environ.get('DB_PORT', '3306'),
            database=os.environ.get('DB_USERS_NAME', 'STGM_RAPPORT_REVIZTO_DB')
        )

        if connection.is_connected():
            print(f"[DEBUG] Connected to MySQL database: {connection.database}")
            return connection

    except Error as e:
        print(f"[DEBUG] Error connecting to MySQL: {e}")
        return None