from fastapi import FastAPI, HTTPException, Depends, Query
from typing import Annotated
from app.db import create_db_and_tables, get_session
from app.models import Driver, DriverCreate, DriverUpdate, DriverPublic
from sqlmodel import Session, select


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Create a driver
@app.post("/drivers/", response_model=DriverPublic)
def create_driver(driver: DriverCreate, session: SessionDep):
    db_driver = Driver.model_validate(driver)
    session.add(db_driver)
    session.commit()
    session.refresh(db_driver)
    return db_driver


# Read drivers
@app.get("/drivers/", response_model=list[DriverPublic])
def read_drivers(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    drivers = session.exec(select(Driver).offset(offset).limit(limit)).all()
    return drivers


# Read one driver
@app.get("/drivers/{driver_id}", response_model=DriverPublic)
def read_driver(driver_id: int, session: SessionDep):
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


# Update a driver
@app.patch("/drivers/{driver_id}", response_model=DriverPublic)
def update_driver(driver_id: int, driver: DriverUpdate, session: SessionDep):
    driver_db = session.get(Driver, driver_id)
    if not driver_db:
        raise HTTPException(status_code=404, detail="Driver not found")
    driver_data = driver.model_dump(exclude_unset=True)
    driver_db.sqlmodel_update(driver_data)
    session.add(driver_db)
    session.commit()
    session.refresh(driver_db)
    return driver_db


# Delete a driver
@app.delete("/drivers/{driver_id}")
def delete_driver(driver_id: int, session: SessionDep):
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    session.delete(driver)
    session.commit()
    return {"ok": True}
