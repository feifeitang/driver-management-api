from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Annotated
from app.db import get_session
from app.db.models import Driver, DriverCreate, DriverUpdate, DriverPublic
from sqlmodel import Session, select


router = APIRouter(prefix="/drivers", tags=["drivers"])

SessionDep = Annotated[Session, Depends(get_session)]


# Create a driver
@router.post("/", response_model=DriverPublic)
def create_driver(driver: DriverCreate, session: SessionDep):
    db_driver = Driver.model_validate(driver)
    session.add(db_driver)
    session.commit()
    session.refresh(db_driver)
    return db_driver


# Read drivers
@router.get("/", response_model=list[DriverPublic])
def read_drivers(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    drivers = session.exec(select(Driver).offset(offset).limit(limit)).all()
    return drivers


# Read one driver
@router.get("/{driver_id}", response_model=DriverPublic)
def read_driver(driver_id: int, session: SessionDep):
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


# Update a driver
@router.patch("/{driver_id}", response_model=DriverPublic)
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
@router.delete("/{driver_id}")
def delete_driver(driver_id: int, session: SessionDep):
    driver = session.get(Driver, driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    session.delete(driver)
    session.commit()
    return {"ok": True}
