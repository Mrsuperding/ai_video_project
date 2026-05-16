"""
Script API Tests - TC-SCRIPT-001 to TC-SCRIPT-009
"""
import pytest
from fastapi.testclient import TestClient


class TestScriptAPI:
    """文案脚本测试用例"""

    def test_create_script(self, client: TestClient, auth_headers: dict):
        """TC-SCRIPT-001: 创建脚本"""
        response = client.post(
            "/api/v1/scripts",
            headers=auth_headers,
            json={
                "title": "商品推荐脚本",
                "content": {
                    "segments": [
                        {"id": "seg_001", "text": "大家好，今天给大家推荐一款好物。", "speed": 1.0, "emotion": "happy", "pause_after": 0.5},
                        {"id": "seg_002", "text": "这款产品的最大特点是轻薄便携。", "speed": 0.9, "emotion": "neutral", "pause_after": 0.3}
                    ]
                },
                "language": "zh",
                "category": "marketing"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "id" in data.get("data", {})

    def test_get_scripts_by_category(self, client: TestClient, auth_headers: dict):
        """TC-SCRIPT-002: 获取脚本列表 — 按分类过滤"""
        response = client.get(
            "/api/v1/scripts?category=marketing&page=1&page_size=10",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "items" in data.get("data", {})

    def test_update_script(self, client: TestClient, auth_headers: dict):
        """TC-SCRIPT-003: 更新脚本"""
        # 先创建
        create_resp = client.post(
            "/api/v1/scripts",
            headers=auth_headers,
            json={
                "title": "原始标题",
                "content": {"segments": [{"id": "1", "text": "测试内容"}]},
                "language": "zh"
            }
        )
        script_id = create_resp.json().get("data", {}).get("id", 1)

        response = client.patch(
            f"/api/v1/scripts/{script_id}",
            headers=auth_headers,
            json={"title": "修改后的标题"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_delete_script(self, client: TestClient, auth_headers: dict):
        """TC-SCRIPT-004: 删除脚本"""
        # 先创建
        create_resp = client.post(
            "/api/v1/scripts",
            headers=auth_headers,
            json={"title": "待删除脚本", "content": {"segments": []}, "language": "zh"}
        )
        script_id = create_resp.json().get("data", {}).get("id", 1)

        response = client.delete(
            f"/api/v1/scripts/{script_id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_save_as_template(self, client: TestClient, auth_headers: dict):
        """TC-SCRIPT-005: 保存脚本为模板"""
        # 先创建脚本
        create_resp = client.post(
            "/api/v1/scripts",
            headers=auth_headers,
            json={"title": "模板脚本", "content": {"segments": []}, "language": "zh"}
        )
        script_id = create_resp.json().get("data", {}).get("id", 1)

        response = client.post(
            f"/api/v1/scripts/{script_id}/save-as-template",
            headers=auth_headers,
            json={"title": "我的模板", "description": "通用推荐模板", "category": "marketing"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_ai_generate(self, client: TestClient, auth_headers: dict):
        """TC-SCRIPT-006: AI 生成文案"""
        response = client.post(
            "/api/v1/ai-writing/generate",
            headers=auth_headers,
            json={
                "topic": "降噪耳机推荐",
                "scene": "marketing",
                "keywords": ["降噪", "舒适", "音质"],
                "language": "zh",
                "length": "medium"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_ai_rewrite(self, client: TestClient, auth_headers: dict):
        """TC-SCRIPT-007: AI 改写文案"""
        response = client.post(
            "/api/v1/ai-writing/rewrite",
            headers=auth_headers,
            json={
                "text": "这个耳机很好用",
                "task_type": "polish",
                "style": "professional"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_script_templates(self, client: TestClient, auth_headers: dict):
        """TC-SCRIPT-008: 获取脚本模板列表"""
        response = client.get(
            "/api/v1/script-templates/list?category=marketing&source=platform",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_template_detail(self, client: TestClient, auth_headers: dict):
        """TC-SCRIPT-009: 获取模板详情"""
        response = client.get(
            "/api/v1/script-templates/1",
            headers=auth_headers
        )
        assert response.status_code == 200