from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from .db import init_database, default_employees
from .routes.employees import router as employee_router

from backend.routes.employees import router as employee_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('origin'),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_database()
    default_employees()


app.include_router(employee_router)
