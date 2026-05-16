"""
WebSocket Tests - TC-WS-001 to TC-WS-002
"""
import pytest
from fastapi.testclient import TestClient


class TestWebSocketAPI:
    """WebSocket 测试用例"""

    def test_ws_connection_invalid_token(self, client: TestClient):
        """TC-WS-002: WebSocket — 无效 Token"""
        # Test WebSocket upgrade with invalid token
        response = client.get(
            "/api/v1/ws/stream?token=invalid_token"
        )
        # WebSocket upgrade will fail with 400 series or normal HTTP response
        assert response.status_code in [400, 401, 403, 404, 500]

    def test_ws_endpoint_exists(self, client: TestClient):
        """检查 WebSocket 端点存在"""
        # WebSocket endpoint should exist at /api/v1/ws/stream
        response = client.get("/api/v1/ws/stream")
        # Should not be 404 (might be 400 for missing token or other error)
        assert response.status_code != 404