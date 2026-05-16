"""
User API Tests - TC-USER-001 to TC-USER-010
"""
import pytest
from fastapi.testclient import TestClient


class TestUserAPI:
    """用户管理测试用例"""

    def test_get_profile(self, client: TestClient, auth_headers: dict):
        """TC-USER-001: 获取个人资料"""
        response = client.get("/api/v1/user/profile", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        user = data.get("data", {})
        assert "id" in user
        assert "phone" in user
        assert "nickname" in user
        assert "password_hash" not in str(data)  # 不应返回密码

    def test_update_profile(self, client: TestClient, auth_headers: dict):
        """TC-USER-002: 修改个人资料"""
        response = client.patch(
            "/api/v1/user/profile",
            headers=auth_headers,
            json={"nickname": "测试用户A", "bio": "这是我的简介"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_change_password_first_time(self, client: TestClient, auth_headers: dict):
        """TC-USER-003: 修改密码 — 首次设置"""
        response = client.post(
            "/api/v1/user/password/change",
            headers=auth_headers,
            json={"old_password": "", "new_password": "NewPass123!"}
        )
        assert response.status_code == 200

    def test_change_password_wrong_old(self, client: TestClient, auth_headers: dict):
        """TC-USER-004: 修改密码 — 旧密码错误"""
        response = client.post(
            "/api/v1/user/password/change",
            headers=auth_headers,
            json={"old_password": "WrongOld123", "new_password": "NewPass456!"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") != 0

    def test_get_devices(self, client: TestClient, auth_headers: dict):
        """TC-USER-005: 获取设备列表"""
        response = client.get("/api/v1/user/devices", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "items" in data.get("data", {})

    def test_bind_phone(self, client: TestClient, auth_headers: dict):
        """TC-USER-007: 绑定手机号"""
        # 先发送验证码
        client.post("/api/v1/auth/sms/send", json={
            "phone": "13900139001",
            "code_type": "bind"
        })
        response = client.post(
            "/api/v1/user/phone/bind",
            headers=auth_headers,
            json={"phone": "13900139001", "code": "123456"}
        )
        assert response.status_code == 200

    def test_get_oauth_bindings(self, client: TestClient, auth_headers: dict):
        """TC-USER-008: 获取 OAuth 绑定列表"""
        response = client.get("/api/v1/user/oauth-bindings", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "items" in data.get("data", {})

    def test_unauthorized_profile_access(self, client: TestClient):
        """TC-USER-009: 未登录访问个人资料"""
        response = client.get("/api/v1/user/profile")
        assert response.status_code in [401, 403]

    def test_expired_token_access(self, client: TestClient):
        """TC-USER-010: 过期 Token 访问"""
        response = client.get(
            "/api/v1/user/profile",
            headers={"Authorization": "Bearer invalid_expired_token"}
        )
        assert response.status_code in [401, 403]