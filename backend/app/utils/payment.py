"""
Payment Utilities - WeChat Pay
"""
import time
import random
import string
import hashlib
from typing import Optional

import httpx
from wechatpayv3 import WeChatPay, WeChatPayAsync

from app.config import settings


class PaymentService:
    """WeChat Pay service"""

    def __init__(self):
        self.wxpay = None

    def _generate_nonce(self, length: int = 32) -> str:
        """Generate random nonce string"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def _generate_sign(self, sign_str: str) -> str:
        """Generate sign"""
        md5 = hashlib.md5()
        md5.update((sign_str + settings.WECHAT_API_KEY).encode())
        return md5.hexdigest().upper()

    async def unified_order(
        self,
        out_trade_no: str,
        total_amount: int,
        description: str,
        notify_url: str,
        attach: Optional[str] = None
    ) -> Optional[dict]:
        """Unified order (create payment)"""
        if not settings.WECHAT_APP_ID or not settings.WECHAT_MCH_ID:
            return None

        timestamp = str(int(time.time()))
        nonce = self._generate_nonce()

        params = {
            "appid": settings.WECHAT_APP_ID,
            "mchid": settings.WECHAT_MCH_ID,
            "description": description,
            "out_trade_no": out_trade_no,
            "time_expire": timestamp,
            "amount": {
                "total": total_amount,
                "currency": "CNY"
            },
            "notify_url": notify_url,
            "scene_info": {
                "payer": {"client_ip": "127.0.0.1"}
            }
        }

        if attach:
            params["attach"] = attach

        try:
            wxpay = WeChatPayAsync(
                wechatpay_url="https://api.mch.weixin.qq.com",
                wechatpay_appid=settings.WECHAT_APP_ID,
                wechatpay_mchid=settings.WECHAT_MCH_ID,
                wechatpay_api_key=settings.WECHAT_API_KEY,
                wechatpay_private_key="",
                wechatpay_cert_chain=[]
            )
            code, resp = await wxpay.pay(
                description=description,
                out_trade_no=out_trade_no,
                amount={"total": total_amount, "currency": "CNY"},
                notify_url=notify_url,
                payer={"client_ip": "127.0.0.1"}
            )
            if code == 200:
                return resp
        except Exception:
            pass

        return None

    async def query_order(self, out_trade_no: str) -> Optional[dict]:
        """Query order status"""
        if not settings.WECHAT_APP_ID:
            return None

        try:
            wxpay = WeChatPayAsync(
                wechatpay_url="https://api.mch.weixin.qq.com",
                wechatpay_appid=settings.WECHAT_APP_ID,
                wechatpay_mchid=settings.WECHAT_MCH_ID,
                wechatpay_api_key=settings.WECHAT_API_KEY,
                wechatpay_private_key="",
                wechatpay_cert_chain=[]
            )
            code, resp = await wxpay.query(out_trade_no=out_trade_no)
            if code == 200:
                return resp
        except Exception:
            pass

        return None

    async def close_order(self, out_trade_no: str) -> bool:
        """Close order"""
        if not settings.WECHAT_APP_ID:
            return False

        try:
            wxpay = WeChatPayAsync(
                wechatpay_url="https://api.mch.weixin.qq.com",
                wechatpay_appid=settings.WECHAT_APP_ID,
                wechatpay_mchid=settings.WECHAT_MCH_ID,
                wechatpay_api_key=settings.WECHAT_API_KEY,
                wechatpay_private_key="",
                wechatpay_cert_chain=[]
            )
            code, _ = await wxpay.close(out_trade_no=out_trade_no)
            return code == 204
        except Exception:
            return False


payment_service = PaymentService()