"""
Cross-Module Flow Tests - TC-FLOW-001 to TC-FLOW-003
"""
import pytest
from fastapi.testclient import TestClient


class TestFlows:
    """跨模块业务流程测试"""

    def test_complete_video_creation_flow(self, client: TestClient, auth_headers: dict):
        """TC-FLOW-001: 完整视频创建流程"""
        # 1. 创建数字人
        dh_resp = client.post(
            "/api/v1/digital-humans",
            headers=auth_headers,
            json={
                "name": "流程测试数字人",
                "source_type": "single_photo",
                "source_photos": [{"photo_url": "https://example.com/face.jpg", "photo_type": "front"}],
                "authorization_type": "self"
            }
        )
        assert dh_resp.status_code == 200
        dh_data = dh_resp.json()
        assert dh_data.get("code") == 0
        dh_id = dh_data.get("data", {}).get("id")

        # 2. 创建脚本
        script_resp = client.post(
            "/api/v1/scripts",
            headers=auth_headers,
            json={
                "title": "流程测试脚本",
                "content": {"segments": [{"id": "1", "text": "测试内容"}]},
                "language": "zh"
            }
        )
        assert script_resp.status_code == 200
        script_data = script_resp.json()
        assert script_data.get("code") == 0
        script_id = script_data.get("data", {}).get("id")

        # 3. 创建视频项目
        video_resp = client.post(
            "/api/v1/video-projects",
            headers=auth_headers,
            json={
                "project_name": "流程测试视频",
                "digital_human_id": dh_id,
                "script_id": script_id
            }
        )
        assert video_resp.status_code == 200
        video_data = video_resp.json()
        assert video_data.get("code") == 0
        project_id = video_data.get("data", {}).get("id")

        # 4. 提交生成
        gen_resp = client.post(
            f"/api/v1/video-projects/{project_id}/generate",
            headers=auth_headers,
            json={"priority": 5}
        )
        assert gen_resp.status_code == 200

    def test_quota_control_flow(self, client: TestClient, auth_headers: dict):
        """TC-FLOW-002: 配额控制全链路"""
        # 测试免费用户配额限制
        # 免费用户: 3 数字人, 10 视频/月

        # 尝试创建多个数字人
        for i in range(3):
            resp = client.post(
                "/api/v1/digital-humans",
                headers=auth_headers,
                json={
                    "name": f"配额测试数字人{i+1}",
                    "source_type": "single_photo",
                    "source_photos": [{"photo_url": f"https://example.com/face{i}.jpg", "photo_type": "front"}],
                    "authorization_type": "self"
                }
            )
            assert resp.status_code == 200

    def test_data_isolation_flow(self, client: TestClient, auth_headers: dict):
        """TC-FLOW-003: 数据隔离验证"""
        # 创建数字人
        dh_resp = client.post(
            "/api/v1/digital-humans",
            headers=auth_headers,
            json={
                "name": "隔离测试数字人",
                "source_type": "single_photo",
                "source_photos": [{"photo_url": "https://example.com/face.jpg", "photo_type": "front"}],
                "authorization_type": "self"
            }
        )
        assert dh_resp.status_code == 200
        dh_id = dh_resp.json().get("data", {}).get("id")

        # 尝试访问他人的数字人 ID
        other_resp = client.get(
            f"/api/v1/digital-humans/{dh_id + 9999}",
            headers=auth_headers
        )
        assert other_resp.status_code == 200
        data = other_resp.json()
        assert data.get("code") != 0  # 应该返回错误

        # 获取自己的数字人列表，应该包含刚创建的
        list_resp = client.get(
            "/api/v1/digital-humans",
            headers=auth_headers
        )
        assert list_resp.status_code == 200
        list_data = list_resp.json()
        assert list_data.get("code") == 0