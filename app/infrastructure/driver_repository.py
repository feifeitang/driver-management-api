from sqlmodel import select, Session
from app.domain.driver import Driver
from typing import List, Optional, Tuple
import logging


class DriverRepository:
    """
    Repository class to handle data persistence for the Driver entity.
    """

    def __init__(self, session: Session):
        self.session = session

    def health_check(self) -> Tuple[bool, str]:
        """
        Check if the database connection is healthy.
        """
        try:
            # Set a timeout to avoid waiting too long
            self.session.execute(select(1))
            return True, "Database connection is healthy"
        except Exception as e:
            logging.error(f"Database health check failed: {str(e)}")
            return False, f"Database connection failed: {str(e)}"
        finally:
            # Ensure any incomplete transactions are rolled back
            self.session.rollback()

    def save(self, driver: Driver) -> Driver:
        """
        Save or update a driver in the database.
        """
        self.session.add(driver)
        self.session.commit()
        self.session.refresh(driver)
        return driver

    def get_all(self) -> List[Driver]:
        """
        Retrieve all drivers from the database.
        """
        statement = select(Driver)
        return self.session.exec(statement).all()

    def get_by_id(self, driver_id: int) -> Optional[Driver]:
        """
        Retrieve a driver by ID.
        """
        return self.session.get(Driver, driver_id)

    def delete(self, driver_id: int) -> bool:
        """
        Delete a driver by ID.
        """
        driver = self.get_by_id(driver_id)
        if driver:
            self.session.delete(driver)
            self.session.commit()
            return True
        return False
