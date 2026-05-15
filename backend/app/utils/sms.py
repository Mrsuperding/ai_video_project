"""
SMS Utilities - Aliyun SMS
"""
import json
from typing import Optional

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

from app.config import settings


class SMSService:
    """Aliyun SMS service"""

    def __init__(self):
        self.client = None
        if settings.ALIYUN_ACCESS_KEY and settings.ALIYUN_SECRET_KEY:
            self.client = AcsClient(
                settings.ALIYUN_ACCESS_KEY,
                settings.ALIYUN_SECRET_KEY,
                "default"
            )

    def send_code(
        self,
        phone: str,
        code: str,
        template_code: Optional[str] = None
    ) -> bool:
        """Send verification code"""
        if not self.client:
            return False

        template = template_code or settings.ALIYUN_SMS_TEMPLATE_CODE

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', settings.ALIYUN_SMS_SIGN_NAME)
        request.add_query_param('TemplateCode', template)
        request.add_query_param('TemplateParam', json.dumps({"code": code}))

        try:
            response = self.client.do_action_with_exception(request)
            return True
        except Exception:
            return False

    def send_notification(
        self,
        phone: str,
        template_code: str,
        template_param: dict
    ) -> bool:
        """Send notification SMS"""
        if not self.client:
            return False

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('PhoneNumbers', phone)
        request.add_query_param('SignName', settings.ALIYUN_SMS_SIGN_NAME)
        request.add_query_param('TemplateCode', template_code)
        request.add_query_param('TemplateParam', json.dumps(template_param))

        try:
            self.client.do_action_with_exception(request)
            return True
        except Exception:
            return False


sms_service = SMSService()