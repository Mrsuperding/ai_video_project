"""
Asset API Tests - TC-ASSET-001 to TC-ASSET-007
"""
import pytest
from fastapi.testclient import TestClient


class TestAssetAPI:
    """素材管理测试用例"""

    def test_get_upload_token(self, client: TestClient, auth_headers: dict):
        """TC-ASSET-001: 获取上传凭证"""
        response = client.post(
            "/api/v1/user-assets/token",
            headers=auth_headers,
            json={
                "file_name": "background.jpg",
                "file_size": 2048000,
                "asset_type": "image"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "upload_token" in data.get("data", {})

    def test_get_user_assets(self, client: TestClient, auth_headers: dict):
        """TC-ASSET-003: 获取用户素材列表"""
        response = client.get(
            "/api/v1/user-assets?asset_type=image&page=1",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "items" in data.get("data", {})

    def test_get_platform_assets(self, client: TestClient, auth_headers: dict):
        """TC-ASSET-005: 获取平台素材列表"""
        response = client.get(
            "/api/v1/platform-assets/list?asset_type=background&category=office",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_asset_categories(self, client: TestClient, auth_headers: dict):
        """TC-ASSET-006: 获取素材分类"""
        response = client.get(
            "/api/v1/platform-assets/categories?asset_type=bgm",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_delete_asset(self, client: TestClient, auth_headers: dict):
        """TC-ASSET-004: 删除素材"""
        # 先获取素材列表
        list_resp = client.get("/api/v1/user-assets", headers=auth_headers)
        items = list_resp.json().get("data", {}).get("items", [])
        if items:
            asset_id = items[0].get("id", 1)
            response = client.delete(
                f"/api/v1/user-assets/{asset_id}",
                headers=auth_headers
            )
            assert response.status_code == 200
            data = response.json()
            assert data.get("code") == 0


class TestVoiceAPI:
    """声音克隆测试用例"""

    def test_get_voice_list(self, client: TestClient, auth_headers: dict):
        """获取声音克隆列表"""
        response = client.get(
            "/api/v1/voice-clones?page=1&page_size=10",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_preview_tts(self, client: TestClient, auth_headers: dict):
        """TTS 预览"""
        response = client.post(
            "/api/v1/voice-clones/preview",
            headers=auth_headers,
            json={
                "text": "这是一段测试文本，用于预览TTS效果。",
                "voice_id": None,
                "config": {"speed": 1.0}
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "audio_url" in data.get("data", {})