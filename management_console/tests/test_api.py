import sys
import os
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
import random

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import app
from src.event_simulator import OrderProcessor, UserAuthenticator
from src.models import LogEntry
from src.database_handler import initialize_database

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    """Initialize test database before running tests."""
    initialize_database()
    yield
    # Could add cleanup here if needed

@pytest.fixture
def sample_log_entry():
    """Create a sample log entry for testing."""
    return {
        "source": "TestComponent",
        "log": "Test log message",
        "timestamp": datetime.utcnow().isoformat()
    }

class TestAPIEndpoints:
    """Test suite for API endpoints."""

    def test_create_log(self, setup_database, sample_log_entry):
        """Test creating a new log entry."""
        response = client.post("/logs/", json=sample_log_entry)
        assert response.status_code == 200
        data = response.json()
        assert data["source"] == sample_log_entry["source"]
        assert data["log"] == sample_log_entry["log"]
        assert "uid" in data

    def test_get_log(self, setup_database, sample_log_entry):
        """Test retrieving a specific log entry."""
        # First create a log
        create_response = client.post("/logs/", json=sample_log_entry)
        log_id = create_response.json()["uid"]

        # Then retrieve it
        response = client.get(f"/logs/{log_id}/")
        assert response.status_code == 200
        data = response.json()
        assert data["uid"] == log_id
        assert data["source"] == sample_log_entry["source"]

    def test_get_all_logs(self, setup_database):
        """Test retrieving all log entries."""
        response = client.get("/logs/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_update_log(self, setup_database, sample_log_entry):
        """Test updating a log entry."""
        # First create a log
        create_response = client.post("/logs/", json=sample_log_entry)
        log_id = create_response.json()["uid"]

        # Update it
        updated_data = sample_log_entry.copy()
        updated_data["log"] = "Updated test message"
        response = client.put(f"/logs/{log_id}/", json=updated_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["log"] == "Updated test message"

    def test_delete_log(self, setup_database, sample_log_entry):
        """Test deleting a log entry."""
        # First create a log
        create_response = client.post("/logs/", json=sample_log_entry)
        log_id = create_response.json()["uid"]

        # Delete it
        response = client.delete(f"/logs/{log_id}/")
        assert response.status_code == 200

        # Verify it's deleted
        get_response = client.get(f"/logs/{log_id}/")
        assert get_response.status_code == 404

class TestEventSimulator:
    """Test suite for event simulator components."""

    def test_order_processor(self, setup_database):
        """Test OrderProcessor functionality."""
        processor = OrderProcessor()
        
        # Test successful order processing
        processor.process_order(1001)
        
        # Verify log was created
        response = client.get("/logs/")
        logs = response.json()
        assert any("OrderProcessor" in log["source"] for log in logs)
        assert any("1001" in log["log"] for log in logs)

    def test_user_authenticator(self, setup_database):
        """Test UserAuthenticator functionality."""
        authenticator = UserAuthenticator()
        
        # Test user authentication
        test_user_id = "test_user_123"
        result = authenticator.authenticate_user(test_user_id)
        
        # Verify log was created
        response = client.get("/logs/")
        logs = response.json()
        assert any("UserAuthenticator" in log["source"] for log in logs)
        assert any(test_user_id in log["log"] for log in logs)

    def test_simulator_integration(self, setup_database):
        """Test simulator integration with short duration."""
        from src.event_simulator import run_simulator
        
        # Get initial log count
        initial_response = client.get("/logs/")
        initial_count = len(initial_response.json())
        
        # Run simulator for a short duration
        run_simulator(duration_seconds=5)
        
        # Get final log count
        final_response = client.get("/logs/")
        final_count = len(final_response.json())
        
        # Verify new logs were created
        assert final_count > initial_count

class TestErrorHandling:
    """Test suite for error handling scenarios."""

    def test_get_nonexistent_log(self, setup_database):
        """Test retrieving a non-existent log."""
        response = client.get("/logs/99999/")
        assert response.status_code == 404

    def test_invalid_log_data(self, setup_database):
        """Test creating a log with invalid data."""
        invalid_data = {
            "source": "",  # Empty source should be invalid
            "log": "Test message"
        }
        response = client.post("/logs/", json=invalid_data)
        assert response.status_code in [400, 422]  # FastAPI validation error

    def test_delete_nonexistent_log(self, setup_database):
        """Test deleting a non-existent log."""
        response = client.delete("/logs/99999/")
        assert response.status_code == 404

if __name__ == "__main__":
    pytest.main(["-v"])