from sqlmodel import SQLModel, Field
from typing import Optional
from fastapi import HTTPException


class Driver(SQLModel, table=True):
    """
    Domain model for a driver.
    """

    __tablename__ = "driver"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    secret_name: str

    def validate(
        self,
        name: Optional[str] = None,
        age: Optional[int] = None,
        secret_name: Optional[str] = None,
    ):
        """
        Validate driver details.
        """
        if age is not None:
            if age < 18:
                raise HTTPException(
                    status_code=400, detail="Age must be at least 18"
                )  # Business Rule
            self.age = age
        if secret_name:
            self.secret_name = secret_name
