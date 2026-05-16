"""
Admin API Tests - TC-ADMIN-001 to TC-ADMIN-009
"""
import pytest
from fastapi.testclient import TestClient


class TestAdminAPI:
    """管理后台测试用例"""

    def test_admin_login(self, client: TestClient, admin_headers: dict):
        """TC-ADMIN-001: 管理员登录"""
        # admin_headers fixture already validates login works
        assert admin_headers is not None
        assert "Authorization" in admin_headers

    def test_user_token_cannot_access_admin(self, client: TestClient, auth_headers: dict):
        """TC-ADMIN-002: 普通用户 Token 访问管理接口"""
        response = client.get(
            "/api/v1/admin/users",
            headers=auth_headers
        )
        assert response.status_code in [403, 401]

    def test_get_user_list(self, client: TestClient, admin_headers: dict):
        """TC-ADMIN-003: 获取用户列表"""
        response = client.get(
            "/api/v1/admin/users?page=1&page_size=20&membership_type=free",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "items" in data.get("data", {})

    def test_get_user_detail(self, client: TestClient, admin_headers: dict):
        """TC-ADMIN-004: 获取用户详情"""
        response = client.get(
            "/api/v1/admin/users/1",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_ban_user(self, client: TestClient, admin_headers: dict):
        """TC-ADMIN-005: 封禁用户"""
        response = client.post(
            "/api/v1/admin/users/1/ban",
            headers=admin_headers,
            json={"action": "ban"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_unban_user(self, client: TestClient, admin_headers: dict):
        """TC-ADMIN-006: 解封用户"""
        response = client.post(
            "/api/v1/admin/users/1/ban",
            headers=admin_headers,
            json={"action": "unban"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_pending_reviews(self, client: TestClient, admin_headers: dict):
        """TC-ADMIN-007: 获取待审核列表"""
        response = client.get(
            "/api/v1/admin/reviews/pending?target_type=digital_human",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_approve_review(self, client: TestClient, admin_headers: dict):
        """TC-ADMIN-008: 审核通过"""
        response = client.post(
            "/api/v1/admin/reviews/1/approve",
            headers=admin_headers,
            json={"comment": "审核通过"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_reject_review(self, client: TestClient, admin_headers: dict):
        """TC-ADMIN-009: 审核驳回"""
        response = client.post(
            "/api/v1/admin/reviews/1/reject",
            headers=admin_headers,
            json={"reason": "照片不清晰"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0


class TestAdminStatsAPI:
    """管理后台统计测试用例"""

    def test_get_platform_stats(self, client: TestClient, admin_headers: dict):
        """获取平台统计"""
        response = client.get(
            "/api/v1/user/statistics/platform",
            headers=admin_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_user_stats(self, client: TestClient, auth_headers: dict):
        """获取用户统计"""
        response = client.get(
            "/api/v1/user/statistics",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0