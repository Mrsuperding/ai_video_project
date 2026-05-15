"""
Video API Tests
"""
import pytest
from fastapi.testclient import TestClient


class TestVideoAPI:
    """Test video endpoints"""

    def test_get_projects(self, client: TestClient, auth_headers: dict):
        """Test get video projects"""
        response = client.get("/api/v1/video", headers=auth_headers)
        assert response.status_code == 200

    def test_create_project(self, client: TestClient, auth_headers: dict):
        """Test create video project"""
        response = client.post(
            "/api/v1/video",
            headers=auth_headers,
            json={
                "project_name": "Test Project",
                "script_id": 1,
                "digital_human_id": 1
            }
        )
        assert response.status_code == 200

    def test_get_project_detail(self, client: TestClient, auth_headers: dict):
        """Test get project detail"""
        response = client.get("/api/v1/video/1", headers=auth_headers)
        assert response.status_code in [200, 404]