"""
API Tests for 留声画
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealth:
    """Health check endpoint"""

    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestAuth:
    """Authentication endpoints"""

    def test_register(self):
        response = client.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "test123",
            "nickname": "testuser"
        })
        assert response.status_code in [200, 400]  # 400 if already exists

    def test_login(self):
        # First register
        client.post("/api/v1/auth/register", json={
            "email": "logintest@example.com",
            "password": "test123",
            "nickname": "logintest"
        })
        # Then login
        response = client.post("/api/v1/auth/login", data={
            "username": "logintest@example.com",
            "password": "test123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()


class TestTasks:
    """Task management endpoints"""

    def setup_method(self):
        """Get auth token for tests"""
        # Register and login
        client.post("/api/v1/auth/register", json={
            "email": f"tasktest_{id(self)}@example.com",
            "password": "test123",
            "nickname": "tasktest"
        })
        response = client.post("/api/v1/auth/login", data={
            "username": f"tasktest_{id(self)}@example.com",
            "password": "test123"
        })
        self.token = response.json().get("access_token", "")

    def test_list_tasks(self):
        response = client.get(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 200
        assert "tasks" in response.json()

    def test_list_tasks_unauthorized(self):
        response = client.get("/api/v1/tasks")
        assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
