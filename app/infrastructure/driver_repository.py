from sqlmodel import select, Session
from app.domain.driver import Driver
from typing import List, Optional


class DriverRepository:
    """
    Repository class to handle data persistence for the Driver entity.
    """

    def __init__(self, session: Session):
        self.session = session

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
