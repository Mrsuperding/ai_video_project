"""
Digital Human API Tests - TC-DH-001 to TC-DH-010
"""
import pytest
from fastapi.testclient import TestClient


class TestDigitalHumanAPI:
    """数字人管理测试用例"""

    def test_create_digital_human_self(self, client: TestClient, auth_headers: dict):
        """TC-DH-001: 创建数字人 — 自己的照片"""
        response = client.post(
            "/api/v1/digital-humans",
            headers=auth_headers,
            json={
                "name": "我的数字人A",
                "source_type": "single_photo",
                "source_photos": [
                    {"photo_url": "https://oss.example.com/test/face01.jpg", "photo_type": "front"}
                ],
                "authorization_type": "self",
                "gender": "male"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "id" in data.get("data", {})
        assert "task_id" in data.get("data", {})

    def test_create_digital_human_others(self, client: TestClient, auth_headers: dict):
        """TC-DH-003: 创建数字人 — 他人照片需要授权"""
        response = client.post(
            "/api/v1/digital-humans",
            headers=auth_headers,
            json={
                "name": "朋友数字人",
                "source_photos": [{"photo_url": "https://oss.example.com/test/face02.jpg", "photo_type": "front"}],
                "authorization_type": "others",
                "authorization_proof_url": "https://oss.example.com/proof/auth_letter.pdf"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_digital_human_list(self, client: TestClient, auth_headers: dict):
        """TC-DH-004: 获取数字人列表"""
        response = client.get(
            "/api/v1/digital-humans?status=all&page=1&page_size=10",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "items" in data.get("data", {})
        assert "pagination" in data.get("data", {})

    def test_get_digital_human_detail(self, client: TestClient, auth_headers: dict):
        """TC-DH-005: 获取数字人详情"""
        # 先创建一个
        create_resp = client.post(
            "/api/v1/digital-humans",
            headers=auth_headers,
            json={
                "name": "测试数字人",
                "source_type": "single_photo",
                "source_photos": [{"photo_url": "https://example.com/face.jpg", "photo_type": "front"}],
                "authorization_type": "self"
            }
        )
        dh_id = create_resp.json().get("data", {}).get("id", 1)

        response = client.get(
            f"/api/v1/digital-humans/{dh_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_other_user_digital_human(self, client: TestClient, auth_headers: dict):
        """TC-DH-006: 获取他人的数字人 — 应拒绝"""
        response = client.get(
            "/api/v1/digital-humans/999999",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") != 0  # 应该返回错误

    def test_set_default_digital_human(self, client: TestClient, auth_headers: dict):
        """TC-DH-007: 设为默认数字人"""
        # 先创建一个
        create_resp = client.post(
            "/api/v1/digital-humans",
            headers=auth_headers,
            json={
                "name": "默认测试数字人",
                "source_type": "single_photo",
                "source_photos": [{"photo_url": "https://example.com/face.jpg", "photo_type": "front"}],
                "authorization_type": "self"
            }
        )
        dh_id = create_resp.json().get("data", {}).get("id", 1)

        response = client.post(
            f"/api/v1/digital-humans/{dh_id}/set-default",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_delete_digital_human(self, client: TestClient, auth_headers: dict):
        """TC-DH-008: 删除数字人"""
        # 先创建一个
        create_resp = client.post(
            "/api/v1/digital-humans",
            headers=auth_headers,
            json={
                "name": "待删除数字人",
                "source_type": "single_photo",
                "source_photos": [{"photo_url": "https://example.com/face.jpg", "photo_type": "front"}],
                "authorization_type": "self"
            }
        )
        dh_id = create_resp.json().get("data", {}).get("id", 1)

        response = client.delete(
            f"/api/v1/digital-humans/{dh_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_task_progress(self, client: TestClient, auth_headers: dict):
        """TC-DH-009: 查询生成任务进度"""
        # 先创建一个数字人，获取 task_id
        create_resp = client.post(
            "/api/v1/digital-humans",
            headers=auth_headers,
            json={
                "name": "进度测试数字人",
                "source_type": "single_photo",
                "source_photos": [{"photo_url": "https://example.com/face.jpg", "photo_type": "front"}],
                "authorization_type": "self"
            }
        )
        task_id = create_resp.json().get("data", {}).get("task_id", 1)

        response = client.get(
            f"/api/v1/digital-humans/tasks/{task_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_regenerate_digital_human(self, client: TestClient, auth_headers: dict):
        """TC-DH-010: 重新生成数字人"""
        # 先创建一个
        create_resp = client.post(
            "/api/v1/digital-humans",
            headers=auth_headers,
            json={
                "name": "待重新生成数字人",
                "source_type": "single_photo",
                "source_photos": [{"photo_url": "https://example.com/face.jpg", "photo_type": "front"}],
                "authorization_type": "self"
            }
        )
        dh_id = create_resp.json().get("data", {}).get("id", 1)

        response = client.post(
            f"/api/v1/digital-humans/{dh_id}/regenerate",
            headers=auth_headers,
            json={
                "new_photos": [
                    {"photo_url": "https://oss.example.com/test/face02.jpg", "photo_type": "front"}
                ]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_check_photos(self, client: TestClient, auth_headers: dict):
        """TC-DH: 照片检查 API"""
        response = client.post(
            "/api/v1/digital-humans/check-photos",
            headers=auth_headers,
            json={"photo_urls": ["https://example.com/photo1.jpg", "https://example.com/photo2.jpg"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_upload_token(self, client: TestClient, auth_headers: dict):
        """TC-DH: 获取上传凭证"""
        response = client.post(
            "/api/v1/digital-humans/upload/token",
            headers=auth_headers,
            json={}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0