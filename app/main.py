from fastapi import FastAPI
from app.infrastructure import create_db_and_tables
from app.api import drivers


app = FastAPI()


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Include the drivers API router
app.include_router(drivers.router)
