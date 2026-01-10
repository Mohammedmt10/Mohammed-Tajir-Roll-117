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
    conn = mysql.connector.connect(**ROOT_CONFIG)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        
    cursor.close()
    conn.close()

def default_employees():
    conn = mysql.connector.connect(**ROOT_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                role VARCHAR(50)
            )
        """)
    
    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]

    if count == 0:
        employees = [
            ("Ayaan Khan", "ayaan@example.com", "Developer"),
            ("Sara Ali", "sara@example.com", "Designer"),
            ("Rahul Mehta", "rahul@example.com", "Manager"),
            ("Neha Sharma", "neha@example.com", "HR"),
            ("Arjun Patel", "arjun@example.com", "QA"),
            ("Fatima Noor", "fatima@example.com", "DevOps"),
        ]

        cursor.executemany(
            "INSERT INTO employees (name, email, role) VALUES (%s, %s, %s)",
            employees
        )
        conn.commit()
    cursor.close()
    conn.close()


def get_db():
    conn = mysql.connector.connect(**ROOT_CONFIG)
    try:
        yield conn
    finally:
        conn.close()
