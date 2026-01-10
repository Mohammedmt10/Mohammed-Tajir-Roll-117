import os
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")

ROOT_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

connection_pool = None


def init_database():
    """Create database if it does not exist"""
    conn = mysql.connector.connect(**ROOT_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()
    conn.close()


def init_pool():
    """Initialize MySQL connection pool"""
    global connection_pool
    if connection_pool is None:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="employee_pool",
            pool_size=10,
            pool_reset_session=True,
            host=ROOT_CONFIG["host"],
            port=ROOT_CONFIG["port"],
            user=ROOT_CONFIG["user"],
            password=ROOT_CONFIG["password"],
            database=DB_NAME,
        )


def get_raw_connection():
    """Used internally (startup logic)"""
    if connection_pool is None:
        raise RuntimeError("DB pool not initialized")
    return connection_pool.get_connection()


def get_db():
    """FastAPI dependency"""
    conn = get_raw_connection()
    try:
        yield conn
    finally:
        conn.close()
