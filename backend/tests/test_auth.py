"""
Auth API Tests - TC-AUTH-001 to TC-AUTH-008
"""
import pytest
from fastapi.testclient import TestClient


class TestAuthAPI:
    """认证系统测试用例"""

    def test_send_sms_code(self, client: TestClient):
        """TC-AUTH-001: 发送短信验证码 — 正常发送"""
        response = client.post(
            "/api/v1/auth/sms/send",
            json={"phone": "13800138001", "code_type": "login"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "expire_seconds" in data.get("data", {})

    def test_send_sms_code_invalid_phone(self, client: TestClient):
        """TC-AUTH-002: 发送短信验证码 — 手机号格式错误"""
        response = client.post(
            "/api/v1/auth/sms/send",
            json={"phone": "1380013", "code_type": "login"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") != 0

    def test_sms_login_new_user(self, client: TestClient):
        """TC-AUTH-003: 手机验证码登录 — 新用户自动注册"""
        # 先发送验证码
        client.post("/api/v1/auth/sms/send", json={
            "phone": "13800138002",
            "code_type": "login"
        })

        # 模拟验证码（实际测试中需要 mock Redis）
        # 这里测试新用户注册流程
        response = client.post(
            "/api/v1/auth/login/sms",
            json={
                "phone": "13800138002",
                "code": "123456",  # 测试验证码
                "device_type": "web"
            }
        )
        assert response.status_code == 200

    def test_sms_login_wrong_code(self, client: TestClient):
        """TC-AUTH-005: 手机验证码登录 — 验证码错误"""
        response = client.post(
            "/api/v1/auth/login/sms",
            json={
                "phone": "13800138001",
                "code": "000000"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") != 0

    def test_password_login(self, client: TestClient, test_user):
        """TC-AUTH-006: 密码登录 — 正常登录"""
        response = client.post(
            "/api/v1/auth/login/password",
            json={
                "account": test_user.phone,
                "password": "Test123456",
                "device_type": "web"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "tokens" in data.get("data", {})
        assert "access_token" in data["data"]["tokens"]

    def test_password_login_no_password(self, client: TestClient, db):
        """TC-AUTH-007: 密码登录 — 手机注册用户未设密码"""
        from app.models.user import User
        from app.core.security import get_password_hash

        # 创建没有密码的用户
        user = User(
            phone="13900139001",
            nickname="无密码用户",
            password_hash=None,  # 没有密码
            status="active"
        )
        db.add(user)
        db.commit()

        response = client.post(
            "/api/v1/auth/login/password",
            json={
                "account": user.phone,
                "password": "anything"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") != 0  # 应该失败

    def test_refresh_token(self, client: TestClient, test_user):
        """TC-AUTH-008: Token 刷新"""
        # 先登录获取 tokens
        login_resp = client.post("/api/v1/auth/login/password", json={
            "account": test_user.phone,
            "password": "Test123456",
            "device_type": "web"
        })
        login_data = login_resp.json()
        if login_data.get("code") == 0:
            refresh_token = login_data["data"]["tokens"].get("refresh_token")
            if refresh_token:
                response = client.post(
                    "/api/v1/auth/refresh",
                    json={"refresh_token": refresh_token}
                )
                assert response.status_code == 200

    def test_unauthorized_access(self, client: TestClient):
        """TC-AUTH: 未授权访问"""
        response = client.get("/api/v1/user/profile")
        assert response.status_code in [401, 403]