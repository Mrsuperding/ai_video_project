"""
User API Tests
"""
import pytest
from fastapi.testclient import TestClient


class TestUserAPI:
    """Test user endpoints"""

    def test_get_profile(self, client: TestClient, auth_headers: dict):
        """Test get user profile"""
        response = client.get("/api/v1/user/profile", headers=auth_headers)
        assert response.status_code == 200

    def test_update_profile(self, client: TestClient, auth_headers: dict):
        """Test update user profile"""
        response = client.patch(
            "/api/v1/user/profile",
            headers=auth_headers,
            json={"nickname": "Test User"}
        )
        assert response.status_code == 200

    def test_update_avatar(self, client: TestClient, auth_headers: dict):
        """Test update avatar"""
        response = client.post(
            "/api/v1/user/avatar",
            headers=auth_headers,
            json={"avatar_url": "https://example.com/avatar.jpg"}
        )
        assert response.status_code == 200

    def test_change_password(self, client: TestClient, auth_headers: dict):
        """Test change password"""
        response = client.post(
            "/api/v1/user/password",
            headers=auth_headers,
            json={
                "old_password": "OldPass123",
                "new_password": "NewPass123"
            }
        )
        assert response.status_code == 200