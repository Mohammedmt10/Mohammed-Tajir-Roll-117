from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import Optional
import mysql.connector

from ..db import get_db

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", status_code=status.HTTP_200_OK)
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

    # Always return array (frontend-safe)
    return rows


@router.post("/", status_code=status.HTTP_201_CREATED)
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
