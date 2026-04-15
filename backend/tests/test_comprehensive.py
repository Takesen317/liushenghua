"""
Comprehensive API Tests for 留声画
Tests all core functionality: auth, files, tasks, share
"""
import pytest
import uuid
import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def generate_unique_email():
    """Generate unique email for each test"""
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


class TestAuthFlow:
    """Complete authentication flow tests"""

    def test_register_login_me_flow(self):
        """Test complete auth flow: register -> login -> access protected resource"""
        email = generate_unique_email()
        password = "test123456"
        nickname = "testuser"

        # 1. Register - returns access_token directly
        response = client.post("/api/v1/auth/register", json={
            "email": email,
            "password": password,
            "nickname": nickname
        })
        assert response.status_code == 200
        data = response.json()
        # Register returns token directly (not user object)
        assert "access_token" in data
        token = data["access_token"]

        # 2. Login
        response = client.post("/api/v1/auth/login", data={
            "username": email,
            "password": password
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

        # 3. Access protected resource with token
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["email"] == email

    def test_login_with_wrong_password(self):
        """Test login fails with wrong password"""
        email = generate_unique_email()

        # Register first
        client.post("/api/v1/auth/register", json={
            "email": email,
            "password": "correct_password",
            "nickname": "test"
        })

        # Try login with wrong password
        response = client.post("/api/v1/auth/login", data={
            "username": email,
            "password": "wrong_password"
        })
        assert response.status_code == 401

    def test_register_duplicate_email(self):
        """Test cannot register with same email twice"""
        email = generate_unique_email()

        # First registration should succeed
        response = client.post("/api/v1/auth/register", json={
            "email": email,
            "password": "test123",
            "nickname": "test"
        })
        assert response.status_code == 200

        # Second registration with same email should fail
        response = client.post("/api/v1/auth/register", json={
            "email": email,
            "password": "test456",
            "nickname": "test2"
        })
        assert response.status_code == 400


class TestFileOperations:
    """File upload and management tests"""

    def setup_method(self):
        """Get auth token for file tests"""
        email = generate_unique_email()
        client.post("/api/v1/auth/register", json={
            "email": email,
            "password": "test123",
            "nickname": "filetest"
        })
        response = client.post("/api/v1/auth/login", data={
            "username": email,
            "password": "test123"
        })
        self.token = response.json().get("access_token", "")

    def test_upload_file(self):
        """Test file upload"""
        # Create a small test image (1x1 pixel PNG)
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

        response = client.post(
            "/api/v1/files/upload",
            files={"file": ("test.png", io.BytesIO(png_data), "image/png")},
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 200
        data = response.json()
        # FileUploadResponse uses file_id, not id
        assert "file_id" in data
        self.file_id = data["file_id"]

    def test_upload_file_unauthorized(self):
        """Test file upload without token fails"""
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

        response = client.post(
            "/api/v1/files/upload",
            files={"file": ("test.png", io.BytesIO(png_data), "image/png")}
        )
        assert response.status_code == 401

    def test_get_file(self):
        """Test getting file details"""
        # Upload a file first
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        response = client.post(
            "/api/v1/files/upload",
            files={"file": ("test.png", io.BytesIO(png_data), "image/png")},
            headers={"Authorization": f"Bearer {self.token}"}
        )
        file_id = response.json().get("file_id")

        # Get file details
        response = client.get(
            f"/api/v1/files/{file_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == file_id


class TestTaskOperations:
    """Task creation and management tests"""

    def setup_method(self):
        """Get auth token and file_id for task tests"""
        email = generate_unique_email()
        client.post("/api/v1/auth/register", json={
            "email": email,
            "password": "test123",
            "nickname": "tasktest"
        })
        response = client.post("/api/v1/auth/login", data={
            "username": email,
            "password": "test123"
        })
        self.token = response.json().get("access_token", "")

        # Upload a file first
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        response = client.post(
            "/api/v1/files/upload",
            files={"file": ("test.png", io.BytesIO(png_data), "image/png")},
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.file_id = response.json().get("file_id", "")

    def test_create_task(self):
        """Test task creation"""
        response = client.post(
            "/api/v1/tasks",
            json={
                "file_id": self.file_id,
                "style": "warm",
                "voice": "xiaoxiao",
                "music_style": "gentle"
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data
        self.task_id = data["task_id"]
        assert data["status"] in ["pending", "processing", "completed", "failed"]

    def test_get_task(self):
        """Test getting task details"""
        # Create a task first
        response = client.post(
            "/api/v1/tasks",
            json={
                "file_id": self.file_id,
                "style": "warm",
                "voice": "xiaoxiao",
                "music_style": "gentle"
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        task_id = response.json()["task_id"]

        # Get task details
        response = client.get(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert "status" in data

    def test_get_task_status(self):
        """Test getting task status"""
        # Create a task first
        response = client.post(
            "/api/v1/tasks",
            json={
                "file_id": self.file_id,
                "style": "warm",
                "voice": "xiaoxiao",
                "music_style": "gentle"
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        task_id = response.json()["task_id"]

        # Get task status
        response = client.get(
            f"/api/v1/tasks/{task_id}/status",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["task_id"] == task_id
        assert "status" in data
        assert "progress" in data

    def test_list_tasks(self):
        """Test listing user tasks"""
        response = client.get(
            "/api/v1/tasks",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert isinstance(data["tasks"], list)

    def test_delete_task(self):
        """Test task deletion - CRITICAL TEST for the bug we fixed"""
        # Create a task first
        response = client.post(
            "/api/v1/tasks",
            json={
                "file_id": self.file_id,
                "style": "warm",
                "voice": "xiaoxiao",
                "music_style": "gentle"
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        task_id = response.json()["task_id"]

        # Delete the task
        response = client.delete(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("message") == "任务已删除"

        # Verify task is deleted
        response = client.get(
            f"/api/v1/tasks/{task_id}",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 404

    def test_delete_task_unauthorized(self):
        """Test deleting task without authorization fails"""
        # Create a task
        response = client.post(
            "/api/v1/tasks",
            json={
                "file_id": self.file_id,
                "style": "warm",
                "voice": "xiaoxiao",
                "music_style": "gentle"
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        task_id = response.json()["task_id"]

        # Try to delete without token
        response = client.delete(f"/api/v1/tasks/{task_id}")
        assert response.status_code == 401

    def test_delete_nonexistent_task(self):
        """Test deleting non-existent task returns 404"""
        response = client.delete(
            "/api/v1/tasks/nonexistent_task_id",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 404

    def test_retry_task_not_found(self):
        """Test retrying a non-existent task returns 404"""
        response = client.post(
            "/api/v1/tasks/nonexistent_task_id/retry",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 404

    def test_cancel_task_not_found(self):
        """Test cancelling a non-existent task returns 404"""
        response = client.post(
            "/api/v1/tasks/nonexistent_task_id/cancel",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 404

    def test_get_nonexistent_task(self):
        """Test getting a non-existent task returns 404"""
        response = client.get(
            "/api/v1/tasks/nonexistent_task_id",
            headers={"Authorization": f"Bearer {self.token}"}
        )
        assert response.status_code == 404


class TestShareOperations:
    """Share functionality tests"""

    def setup_method(self):
        """Get auth token for share tests"""
        email = generate_unique_email()
        client.post("/api/v1/auth/register", json={
            "email": email,
            "password": "test123",
            "nickname": "sharetest"
        })
        response = client.post("/api/v1/auth/login", data={
            "username": email,
            "password": "test123"
        })
        self.token = response.json().get("access_token", "")

        # Upload a file and create a task
        png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        response = client.post(
            "/api/v1/files/upload",
            files={"file": ("test.png", io.BytesIO(png_data), "image/png")},
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.file_id = response.json().get("file_id", "")

        response = client.post(
            "/api/v1/tasks",
            json={
                "file_id": self.file_id,
                "style": "warm",
                "voice": "xiaoxiao",
                "music_style": "gentle"
            },
            headers={"Authorization": f"Bearer {self.token}"}
        )
        self.task_id = response.json().get("task_id", "")

    def test_create_share_link_on_completed_task(self):
        """Test that share link creation succeeds on completed task"""
        # Task ends up completed (with fallback data when AI services fail)
        response = client.post(
            "/api/v1/share",
            json={"task_id": self.task_id},
            headers={"Authorization": f"Bearer {self.token}"}
        )
        # Should succeed because task is completed
        assert response.status_code == 200
        data = response.json()
        assert "share_code" in data
        assert "url" in data
        assert "/share/" in data["url"]

    def test_create_share_link_nonexistent_task(self):
        """Test that share link creation fails for non-existent task"""
        response = client.post(
            "/api/v1/share",
            json={"task_id": "nonexistent_task_id"},
            headers={"Authorization": f"Bearer {self.token}"}
        )
        # Should fail because task doesn't exist
        assert response.status_code == 404


class TestSecurity:
    """Security and authorization tests"""

    def test_access_without_token(self):
        """Test accessing protected endpoints without token"""
        response = client.get("/api/v1/tasks")
        assert response.status_code == 401

        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_access_with_invalid_token(self):
        """Test accessing protected endpoints with invalid token"""
        response = client.get(
            "/api/v1/tasks",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401


class TestHealthEndpoints:
    """Health check and public endpoints"""

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
