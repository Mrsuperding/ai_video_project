"""
Wallet and Payment API Tests - TC-WALLET-001 to TC-WALLET-006
"""
import pytest
from fastapi.testclient import TestClient


class TestWalletAPI:
    """钱包与支付测试用例"""

    def test_get_wallet(self, client: TestClient, auth_headers: dict):
        """TC-WALLET-001: 获取钱包信息"""
        response = client.get(
            "/api/v1/wallet",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        wallet = data.get("data", {})
        assert "balance" in wallet
        assert "frozen_balance" in wallet

    def test_create_recharge_order(self, client: TestClient, auth_headers: dict):
        """TC-WALLET-002: 创建充值订单"""
        response = client.post(
            "/api/v1/wallet/recharge",
            headers=auth_headers,
            json={
                "amount": 100.00,
                "payment_method": "alipay"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "order_no" in data.get("data", {})

    def test_get_recharge_order(self, client: TestClient, auth_headers: dict):
        """TC-WALLET-003: 查询充值订单状态"""
        # 先创建订单
        create_resp = client.post(
            "/api/v1/wallet/recharge",
            headers=auth_headers,
            json={"amount": 50.00, "payment_method": "wechat"}
        )
        order_no = create_resp.json().get("data", {}).get("order_no", "test_order")

        response = client.get(
            f"/api/v1/wallet/recharge/{order_no}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0

    def test_get_transactions(self, client: TestClient, auth_headers: dict):
        """TC-WALLET-004: 获取交易流水"""
        response = client.get(
            "/api/v1/wallet/transactions?page=1&page_size=20",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "items" in data.get("data", {})


class TestMembershipAPI:
    """会员测试用例"""

    def test_get_membership_plans(self, client: TestClient, auth_headers: dict):
        """TC-WALLET-005: 获取会员套餐列表"""
        response = client.get(
            "/api/v1/memberships/plans",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0
        assert "items" in data.get("data", {})

    def test_get_my_membership(self, client: TestClient, auth_headers: dict):
        """TC-WALLET-006: 获取我的会员信息"""
        response = client.get(
            "/api/v1/memberships/my",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0


class TestCouponAPI:
    """优惠券测试用例"""

    def test_get_coupons(self, client: TestClient, auth_headers: dict):
        """获取优惠券列表"""
        response = client.get(
            "/api/v1/coupons?page=1&page_size=10",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("code") == 0