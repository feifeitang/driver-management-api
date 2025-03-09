import pytest
from unittest.mock import Mock, MagicMock
from app.domain.driver_service import DriverService
from app.domain.driver import Driver
from fastapi import HTTPException


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def driver_service(mock_repository):
    return DriverService(mock_repository)


def test_create_driver_success(driver_service, mock_repository):
    """Test successful driver creation"""
    # Arrange
    mock_driver = Driver(id=1, name="John Doe", age=25, secret_name="Speed King")
    mock_repository.save.return_value = mock_driver

    # Act
    result = driver_service.create_driver(
        name="John Doe", age=25, secret_name="Speed King"
    )

    # Assert
    assert result.id == 1
    assert result.name == "John Doe"
    assert result.age == 25
    mock_repository.save.assert_called_once()


def test_create_driver_underage(driver_service):
    """Test driver creation with invalid age"""
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        driver_service.create_driver(name="Young Driver", age=16, secret_name="Kid")

    assert exc_info.value.status_code == 400
    assert "Age must be at least 18" in exc_info.value.detail


def test_get_driver_success(driver_service, mock_repository):
    """Test successful driver retrieval"""
    # Arrange
    mock_driver = Driver(id=1, name="John Doe", age=25, secret_name="Speed King")
    mock_repository.get_by_id.return_value = mock_driver

    # Act
    result = driver_service.get_driver(1)

    # Assert
    assert result.id == 1
    assert result.name == "John Doe"
    mock_repository.get_by_id.assert_called_once_with(1)


def test_get_driver_not_found(driver_service, mock_repository):
    """Test driver retrieval when not found"""
    # Arrange
    mock_repository.get_by_id.return_value = None

    # Act
    result = driver_service.get_driver(999)

    # Assert
    assert result is None
    mock_repository.get_by_id.assert_called_once_with(999)
