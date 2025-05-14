import os
import mysql.connector
from mysql.connector import Error
import psycopg2
from psycopg2 import Error as PgError

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

def get_postgres_db_connection():
    """
    Create a database connection to PostgreSQL
    Returns connection object or None if connection fails
    """
    try:
        connection = psycopg2.connect(
            host="c5hilnj7pn10vb.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
            database="d4qfmqaelhaou",
            user="ue3edpfcrvn1iu",
            password="p927ab6c7ca5f443100468557f9683b9b94ab0cfde3b745a42832502f43672c9e",
            port="5432"
        )

        if connection:
            print(f"[DEBUG] Connected to PostgreSQL database")
            return connection

    except PgError as e:
        print(f"[DEBUG] Error connecting to PostgreSQL: {e}")
        return None