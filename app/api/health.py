from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.infrastructure import get_session
from app.infrastructure.driver_repository import DriverRepository

router = APIRouter()


@router.get("/health", response_model=dict)
def health_check(session: Session = Depends(get_session)):
    """
    Health check endpoint to verify database connection.
    """
    driver_repo = DriverRepository(session)
    is_healthy, message = driver_repo.health_check()

    if is_healthy:
        return {"status": "ok", "message": message}
    else:
        raise HTTPException(status_code=500, detail=message)
