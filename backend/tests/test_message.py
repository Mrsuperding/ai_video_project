"""
Message and Notification API Tests - TC-MSG-001 to TC-MSG-005
"""
import pytest
from fastapi.testclient import TestClient


class TestMessageAPI:
    """消息通知测试用例"""

    def test_get_messages(self, client: TestClient, auth_headers: dict):
        """TC-MSG-001: 获取消息列表"""
        response = client.get(
            "/api/v1/messages?page=1&page_size=20",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "items" in data.get("data", {})

    def test_get_unread_count(self, client: TestClient, auth_headers: dict):
        """TC-MSG-002: 获取未读消息数"""
        response = client.get(
            "/api/v1/messages/unread-count",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "unread_count" in data.get("data", {})

    def test_mark_message_read(self, client: TestClient, auth_headers: dict):
        """TC-MSG-003: 标记单条消息已读"""
        response = client.post(
            "/api/v1/messages/1/read",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_mark_all_read(self, client: TestClient, auth_headers: dict):
        """TC-MSG-004: 全部标记已读"""
        response = client.post(
            "/api/v1/messages/read-all",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_notification_settings(self, client: TestClient, auth_headers: dict):
        """TC-MSG-005: 获取通知设置"""
        response = client.get(
            "/api/v1/notification-settings",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_update_notification_settings(self, client: TestClient, auth_headers: dict):
        """TC-MSG-005: 更新通知设置"""
        response = client.patch(
            "/api/v1/notification-settings",
            headers=auth_headers,
            json={
                "email_task_complete": True,
                "sms_enabled": False
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0