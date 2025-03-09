from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from app.infrastructure import get_session
from app.infrastructure.models import Driver, DriverCreate, DriverUpdate, DriverPublic
from sqlmodel import Session, select
from app.infrastructure.driver_repository import DriverRepository
from app.domain.driver_service import DriverService


router = APIRouter(tags=["drivers"])


def get_driver_service(session: Session = Depends(get_session)):
    """
    Dependency injection to create a DriverService with a session.
    """
    repository = DriverRepository(session)

    # Check the database health
    is_healthy, message = repository.health_check()
    if not is_healthy:
        raise HTTPException(
            status_code=500, detail=f"Database health check failed: {message}"
        )

    return DriverService(repository)


@router.post("/drivers", response_model=DriverPublic)
def create_driver(
    driver: DriverCreate, service: DriverService = Depends(get_driver_service)
):
    """
    Create a new driver.
    """
    return service.create_driver(driver.name, driver.age, driver.secret_name)


@router.get("/drivers", response_model=List[DriverPublic])
def get_drivers(service: DriverService = Depends(get_driver_service)):
    """
    API endpoint to retrieve all drivers.
    """
    return service.get_all_drivers()


@router.get("/driver/{driver_id}", response_model=Driver)
def get_driver(driver_id: int, service: DriverService = Depends(get_driver_service)):
    """
    Retrieve a driver by ID.
    """
    driver = service.get_driver(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return driver


@router.put("/driver/{driver_id}", response_model=DriverUpdate)
def update_driver(
    driver_id: int,
    driver: DriverUpdate,
    service: DriverService = Depends(get_driver_service),
):
    """
    Update an existing driver's details.
    """
    updated_driver = service.update_driver(
        driver_id, driver.name, driver.age, driver.secret_name
    )
    if not updated_driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    return updated_driver


@router.delete("/driver/{driver_id}", response_model=dict)
def delete_driver(driver_id: int, service: DriverService = Depends(get_driver_service)):
    """
    Delete a driver by ID.
    """
    success = service.delete_driver(driver_id)
    if not success:
        raise HTTPException(status_code=404, detail="Driver not found")
    return {"message": "Driver deleted successfully"}
