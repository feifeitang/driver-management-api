from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from app.main import app
from app.domain.driver import Driver
from app.infrastructure.driver_repository import DriverRepository

client = TestClient(app)


@patch("app.api.drivers.get_session")
def test_create_driver_api(mock_get_session):
    """Test create driver API endpoint"""
    # Arrange
    test_driver = {"name": "John Doe", "age": 25, "secret_name": "Speed King"}

    # Mock the repository
    mock_repo = Mock(spec=DriverRepository)
    mock_repo.health_check.return_value = (True, "Healthy")
    mock_repo.save.return_value = Driver(id=1, **test_driver)

    # Mock the session
    mock_session = Mock()
    mock_get_session.return_value = mock_session

    # Act
    with patch("app.api.drivers.DriverRepository", return_value=mock_repo):
        response = client.post("/drivers/", json=test_driver)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == test_driver["name"]
    assert data["age"] == test_driver["age"]


@patch("app.api.drivers.get_session")
def test_create_underage_driver_api(mock_get_session):
    """Test create driver API endpoint with invalid age"""
    # Arrange
    test_driver = {"name": "Young Driver", "age": 16, "secret_name": "Kid"}

    # Mock the repository
    mock_repo = Mock(spec=DriverRepository)
    mock_repo.health_check.return_value = (True, "Healthy")

    # Mock the session
    mock_session = Mock()
    mock_get_session.return_value = mock_session

    # Act
    with patch("app.api.drivers.DriverRepository", return_value=mock_repo):
        response = client.post("/drivers/", json=test_driver)

    # Assert
    assert response.status_code == 400
    assert "Age must be at least 18" in response.json()["detail"]


@patch("app.api.drivers.get_session")
def test_get_driver_api(mock_get_session):
    """Test get driver API endpoint"""
    # Arrange
    mock_driver = Driver(id=1, name="John Doe", age=25, secret_name="Speed King")

    # Mock the repository
    mock_repo = Mock(spec=DriverRepository)
    mock_repo.health_check.return_value = (True, "Healthy")
    mock_repo.get_by_id.return_value = mock_driver

    # Mock the session
    mock_session = Mock()
    mock_get_session.return_value = mock_session

    # Act
    with patch("app.api.drivers.DriverRepository", return_value=mock_repo):
        response = client.get("/driver/1")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "John Doe"


@patch("app.api.drivers.get_session")
def test_update_driver_success(mock_get_session):
    """Test successful driver update"""
    # Arrange
    original_driver = Driver(id=1, name="John Doe", age=25, secret_name="Speed King")
    update_data = {"name": "John Updated", "age": 26, "secret_name": "Lightning"}

    # Mock the repository
    mock_repo = Mock(spec=DriverRepository)
    mock_repo.health_check.return_value = (True, "Healthy")
    mock_repo.get_by_id.return_value = original_driver
    mock_repo.save.return_value = Driver(id=1, **update_data)

    # Mock the session
    mock_session = Mock()
    mock_get_session.return_value = mock_session

    # Act
    with patch("app.api.drivers.DriverRepository", return_value=mock_repo):
        response = client.put("/driver/1", json=update_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["age"] == update_data["age"]
    mock_repo.get_by_id.assert_called_once_with(1)
    mock_repo.save.assert_called_once()


@patch("app.api.drivers.get_session")
def test_update_driver_not_found(mock_get_session):
    """Test update when driver doesn't exist"""
    # Arrange
    update_data = {"name": "John Updated", "age": 26, "secret_name": "Lightning"}

    # Mock the repository
    mock_repo = Mock(spec=DriverRepository)
    mock_repo.health_check.return_value = (True, "Healthy")
    mock_repo.get_by_id.return_value = None  # Driver not found

    # Mock the session
    mock_session = Mock()
    mock_get_session.return_value = mock_session

    # Act
    with patch("app.api.drivers.DriverRepository", return_value=mock_repo):
        response = client.put("/driver/999", json=update_data)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Driver not found"
    mock_repo.get_by_id.assert_called_once_with(999)
    mock_repo.save.assert_not_called()


@patch("app.api.drivers.get_session")
def test_update_driver_invalid_age(mock_get_session):
    """Test update with invalid age"""
    # Arrange
    original_driver = Driver(id=1, name="John Doe", age=25, secret_name="Speed King")
    update_data = {
        "name": "John Updated",
        "age": 16,  # Invalid age
        "secret_name": "Lightning",
    }

    # Mock the repository
    mock_repo = Mock(spec=DriverRepository)
    mock_repo.health_check.return_value = (True, "Healthy")
    mock_repo.get_by_id.return_value = original_driver

    # Mock the session
    mock_session = Mock()
    mock_get_session.return_value = mock_session

    # Act
    with patch("app.api.drivers.DriverRepository", return_value=mock_repo):
        response = client.put("/driver/1", json=update_data)

    # Assert
    assert response.status_code == 400
    assert "Age must be at least 18" in response.json()["detail"]
    mock_repo.save.assert_not_called()


@patch("app.api.drivers.get_session")
def test_delete_driver_success(mock_get_session):
    """Test successful driver deletion"""
    # Arrange
    # Mock the repository
    mock_repo = Mock(spec=DriverRepository)
    mock_repo.health_check.return_value = (True, "Healthy")
    mock_repo.delete.return_value = True

    # Mock the session
    mock_session = Mock()
    mock_get_session.return_value = mock_session

    # Act
    with patch("app.api.drivers.DriverRepository", return_value=mock_repo):
        response = client.delete("/driver/1")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Driver deleted successfully"
    mock_repo.delete.assert_called_once_with(1)


@patch("app.api.drivers.get_session")
def test_delete_driver_not_found(mock_get_session):
    """Test deletion of non-existent driver"""
    # Arrange
    # Mock the repository
    mock_repo = Mock(spec=DriverRepository)
    mock_repo.health_check.return_value = (True, "Healthy")
    mock_repo.delete.return_value = False

    # Mock the session
    mock_session = Mock()
    mock_get_session.return_value = mock_session

    # Act
    with patch("app.api.drivers.DriverRepository", return_value=mock_repo):
        response = client.delete("/driver/999")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Driver not found"
    mock_repo.delete.assert_called_once_with(999)
