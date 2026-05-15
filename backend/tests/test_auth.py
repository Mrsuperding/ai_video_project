"""
Auth API Tests
"""
import pytest
from fastapi.testclient import TestClient


class TestAuthAPI:
    """Test auth endpoints"""

    def test_send_sms_code(self, client: TestClient):
        """Test send SMS code"""
        response = client.post(
            "/api/v1/auth/send-sms",
            json={"phone": "13800138000"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0 or "message" in data

    def test_register(self, client: TestClient):
        """Test user registration"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "phone": "13800138000",
                "password": "Test123456",
                "sms_code": "123456",
                "invite_code": ""
            }
        )
        assert response.status_code == 200

    def test_login(self, client: TestClient):
        """Test login"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "login_key": "13800138000",
                "password": "Test123456",
                "type": "phone"
            }
        )
        assert response.status_code == 200

    def test_refresh_token(self, client: TestClient):
        """Test refresh token"""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "test_refresh_token"}
        )
        assert response.status_code in [200, 401]