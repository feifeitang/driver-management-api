from fastapi import FastAPI
from app.infrastructure import create_db_and_tables
from app.api import drivers, health
from app.infrastructure.apm import init_apm


app = FastAPI()

# Initialize APM using environment variables
init_apm(app)


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Include the drivers API router
app.include_router(drivers.router)
app.include_router(health.router)
