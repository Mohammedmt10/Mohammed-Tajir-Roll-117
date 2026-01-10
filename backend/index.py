from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init_database, init_pool
from .routes.employees import router as employee_router

from backend.routes.employees import router as employee_router

app = FastAPI()

# ✅ CORS for frontend (Vite)
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


app.include_router(employee_router)
