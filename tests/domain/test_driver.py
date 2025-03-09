import pytest
from fastapi import HTTPException
from app.domain.driver import Driver


def test_driver_creation():
    """Test creating a driver with valid data"""
    driver = Driver(name="John Doe", age=25, secret_name="Speed King")
    assert driver.name == "John Doe"
    assert driver.age == 25
    assert driver.secret_name == "Speed King"


def test_driver_age_validation():
    """Test age validation when creating a driver"""
    driver = Driver(name="Young Driver", age=16, secret_name="Kid")

    with pytest.raises(HTTPException) as exc_info:
        driver.validate(age=driver.age)

    assert exc_info.value.status_code == 400
    assert "Age must be at least 18" in exc_info.value.detail


def test_driver_update_validation():
    """Test validation when updating driver age"""
    driver = Driver(name="John Doe", age=25, secret_name="Speed King")

    with pytest.raises(HTTPException) as exc_info:
        driver.validate(age=17)

    assert exc_info.value.status_code == 400
    assert "Age must be at least 18" in exc_info.value.detail
