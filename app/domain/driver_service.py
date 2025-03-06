from typing import List, Optional
from app.infrastructure.driver_repository import DriverRepository
from app.domain.driver import Driver


class DriverService:
    """
    Service class to handle driver-related operations.
    """

    def __init__(self, repository: DriverRepository):
        self.repository = repository

    def create_driver(self, name: str, age: int, secret_name: str) -> Driver:
        """
        Create a new driver and store it in the repository.
        """
        driver = Driver(name=name, age=age, secret_name=secret_name)
        driver.validate(name, age, secret_name)
        return self.repository.save(driver)

    def get_all_drivers(self) -> List[Driver]:
        """
        Retrieve all drivers from the repository.
        """
        return self.repository.get_all()

    def get_driver(self, driver_id: int) -> Optional[Driver]:
        """
        Retrieve a driver by ID.
        """
        return self.repository.get_by_id(driver_id)

    def update_driver(
        self,
        driver_id: int,
        name: Optional[str] = None,
        age: Optional[int] = None,
        secret_name: Optional[str] = None,
    ) -> Optional[Driver]:
        """
        Update an existing driver's details.
        """
        driver = self.repository.get_by_id(driver_id)
        if not driver:
            return None

        driver.validate(name, age, secret_name)
        return self.repository.save(driver)

    def delete_driver(self, driver_id: int) -> bool:
        """
        Delete a driver from the repository.
        """
        return self.repository.delete(driver_id)
