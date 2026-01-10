import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")

ROOT_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": DB_NAME,
}


def init_database():
    conn = mysql.connector.connect(
        host=ROOT_CONFIG["host"],
        port=ROOT_CONFIG["port"],
        user=ROOT_CONFIG["user"],
        password=ROOT_CONFIG["password"],
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.close()
    conn.close()


def get_db():
    conn = mysql.connector.connect(**ROOT_CONFIG)
    try:
        yield conn
    finally:
        conn.close()
