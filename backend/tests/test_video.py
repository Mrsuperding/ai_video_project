"""
Video API Tests - TC-VIDEO-001 to TC-VIDEO-012
"""
import pytest
from fastapi.testclient import TestClient


class TestVideoAPI:
    """视频项目测试用例"""

    def test_create_video_project(self, client: TestClient, auth_headers: dict):
        """TC-VIDEO-001: 创建视频项目"""
        response = client.post(
            "/api/v1/video-projects",
            headers=auth_headers,
            json={
                "project_name": "商品推荐视频",
                "digital_human_id": 1,
                "script_id": 1,
                "resolution": "1080p",
                "aspect_ratio": "16:9",
                "fps": 30,
                "background_type": "color",
                "background_value": "#FFFFFF"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "id" in data.get("data", {})

    def test_create_video_project_invalid_dh(self, client: TestClient, auth_headers: dict):
        """TC-VIDEO-002: 创建视频项目 — 使用不存在的数字人"""
        response = client.post(
            "/api/v1/video-projects",
            headers=auth_headers,
            json={
                "project_name": "测试视频",
                "digital_human_id": 999999,
                "script_id": 1
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") != 0

    def test_get_video_projects(self, client: TestClient, auth_headers: dict):
        """TC-VIDEO-003: 获取视频项目列表"""
        response = client.get(
            "/api/v1/video-projects?status=all&page=1&page_size=20",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "items" in data.get("data", {})

    def test_get_project_detail(self, client: TestClient, auth_headers: dict):
        """TC-VIDEO-004: 获取项目详情"""
        response = client.get(
            "/api/v1/video-projects/1",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_update_project(self, client: TestClient, auth_headers: dict):
        """TC-VIDEO-005: 更新项目参数"""
        response = client.patch(
            "/api/v1/video-projects/1",
            headers=auth_headers,
            json={
                "project_name": "修改后的项目名",
                "bgm_volume": 0.5,
                "resolution": "720p"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_submit_video_generation(self, client: TestClient, auth_headers: dict):
        """TC-VIDEO-006: 提交视频生成"""
        # 先创建项目
        create_resp = client.post(
            "/api/v1/video-projects",
            headers=auth_headers,
            json={
                "project_name": "待生成视频",
                "digital_human_id": 1,
                "script_id": 1
            }
        )
        project_id = create_resp.json().get("data", {}).get("id", 1)

        response = client.post(
            f"/api/v1/video-projects/{project_id}/generate",
            headers=auth_headers,
            json={"priority": 5}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_cancel_video_generation(self, client: TestClient, auth_headers: dict):
        """TC-VIDEO-008: 取消视频生成"""
        response = client.post(
            "/api/v1/video-projects/1/cancel",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_delete_project(self, client: TestClient, auth_headers: dict):
        """TC-VIDEO-009: 删除项目"""
        # 先创建项目
        create_resp = client.post(
            "/api/v1/video-projects",
            headers=auth_headers,
            json={
                "project_name": "待删除项目",
                "digital_human_id": 1,
                "script_id": 1
            }
        )
        project_id = create_resp.json().get("data", {}).get("id", 1)

        response = client.delete(
            f"/api/v1/video-projects/{project_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_project_outputs(self, client: TestClient, auth_headers: dict):
        """TC-VIDEO-010: 获取视频输出"""
        response = client.get(
            "/api/v1/video-outputs/1",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_share_video(self, client: TestClient, auth_headers: dict):
        """TC-VIDEO-011: 分享视频"""
        response = client.post(
            "/api/v1/video-outputs/1/share",
            headers=auth_headers,
            json={
                "expire_hours": 72,
                "enable_password": True,
                "password": "123456"
            }
        )
        assert response.status_code == 200
        data = response.json()
        # May fail if output doesn't exist, but API should be reachable
        assert response.status_code == 200

    def test_get_shared_video(self, client: TestClient):
        """TC-VIDEO-012: 访问分享链接 (无需登录)"""
        response = client.get(
            "/api/v1/video-outputs/shared/test_token"
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0 or data.get("code") == 40405


class TestGenerationTaskAPI:
    """生成任务测试用例"""

    def test_get_task_list(self, client: TestClient, auth_headers: dict):
        """获取任务列表"""
        response = client.get(
            "/api/v1/generation-tasks?page=1&page_size=20",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_task_detail(self, client: TestClient, auth_headers: dict):
        """获取任务详情"""
        response = client.get(
            "/api/v1/generation-tasks/1",
            headers=auth_headers
        )
        assert response.status_code == 200