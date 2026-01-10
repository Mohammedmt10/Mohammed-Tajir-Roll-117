from fastapi import FastAPI, Depends, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import mysql.connector

from db import init_database, init_pool, get_db, get_raw_connection

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_database()
    init_pool()

    conn = get_raw_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            department VARCHAR(100) NOT NULL,
            designation VARCHAR(100) NOT NULL,
            date_of_joining DATE NOT NULL,
            INDEX idx_name (name),
            INDEX idx_department (department)
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM employees")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            """
            INSERT INTO employees
            (name, email, department, designation, date_of_joining)
            VALUES (%s, %s, %s, %s, %s)
            """,
            [
                ("Aman Sharma", "aman@example.com", "Engineering", "Backend Developer", "2023-06-10"),
                ("Priya Verma", "priya@example.com", "HR", "HR Manager", "2022-04-18"),
                ("Rohit Singh", "rohit@example.com", "Finance", "Accountant", "2021-11-01"),
                ("Neha Patel", "neha@example.com", "Marketing", "SEO Specialist", "2024-01-15"),
            ]
        )
        conn.commit()

    cursor.close()
    conn.close()


@app.get("/employees", status_code=status.HTTP_200_OK)
def get_employees(
    search: Optional[str] = Query(None),
    conn=Depends(get_db)
):
    cursor = conn.cursor(dictionary=True)

    if search:
        cursor.execute(
            "SELECT * FROM employees WHERE name LIKE %s",
            (f"%{search}%",)
        )
    else:
        cursor.execute("SELECT * FROM employees")

    rows = cursor.fetchall()
    cursor.close()

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No employees found"
        )

    return rows


@app.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(employee: dict, conn=Depends(get_db)):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO employees
            (name, email, department, designation, date_of_joining)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                employee["name"],
                employee["email"],
                employee["department"],
                employee["designation"],
                employee["date_of_joining"],
            )
        )
        conn.commit()
        cursor.close()

        return {"message": "Employee created successfully"}

    except mysql.connector.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
