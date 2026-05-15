"""
OSS Utilities - Aliyun Cloud Storage
"""
import hashlib
import time
from typing import Optional

import oss2

from app.config import settings


class AliyunOSSService:
    """Aliyun OSS service"""

    def __init__(self):
        self.auth = None
        self.bucket = None
        if settings.ALIYUN_ACCESS_KEY and settings.ALIYUN_SECRET_KEY and settings.ALIYUN_BUCKET:
            self.auth = oss2.Auth(settings.ALIYUN_ACCESS_KEY, settings.ALIYUN_SECRET_KEY)
            self.bucket = oss2.Bucket(
                self.auth,
                f"https://oss-cn-hangzhou.aliyuncs.com" if not settings.ALIYUN_REGION else f"https://oss-{settings.ALIYUN_REGION}.aliyuncs.com",
                settings.ALIYUN_BUCKET
            )

    def generate_upload_token(self, key: str, expires: int = 3600) -> Optional[str]:
        """Generate upload token (for client-side upload)"""
        if not self.bucket:
            return None
        try:
            # Generate a signed URL for upload
            return self.bucket.sign_url("PUT", key, expires)
        except Exception:
            return None

    def generate_download_url(self, key: str, expires: int = 3600) -> Optional[str]:
        """Generate download URL"""
        if not self.bucket:
            return None
        try:
            # Generate a signed URL for download
            return self.bucket.sign_url("GET", key, expires)
        except Exception:
            return None

    def upload_file(self, local_file: str, key: str) -> bool:
        """Upload file to OSS"""
        if not self.bucket:
            return False
        try:
            result = self.bucket.put_object(key, open(local_file, "rb").read())
            return result.status == 200
        except Exception:
            return False

    def upload_data(self, data: bytes, key: str) -> bool:
        """Upload data to OSS"""
        if not self.bucket:
            return False
        try:
            result = self.bucket.put_object(key, data)
            return result.status == 200
        except Exception:
            return False

    def delete_file(self, key: str) -> bool:
        """Delete file from OSS"""
        if not self.bucket:
            return False
        try:
            result = self.bucket.delete_object(key)
            return result.status == 200
        except Exception:
            return False

    def get_file_info(self, key: str) -> Optional[dict]:
        """Get file info"""
        if not self.bucket:
            return None
        try:
            result = self.bucket.get_object_meta(key)
            return {
                "size": result.content_length,
                "last_modified": result.last_modified
            }
        except Exception:
            return None

    def file_exists(self, key: str) -> bool:
        """Check if file exists"""
        if not self.bucket:
            return False
        try:
            return self.bucket.object_exists(key)
        except Exception:
            return False

    @staticmethod
    def generate_key(filename: str, prefix: str = "") -> str:
        """Generate unique file key"""
        timestamp = int(time.time() * 1000)
        ext = filename.split(".")[-1] if "." in filename else ""
        hash_str = hashlib.md5(f"{filename}{timestamp}".encode()).hexdigest()[:8]
        if prefix:
            return f"{prefix}/{timestamp}_{hash_str}.{ext}"
        return f"{timestamp}_{hash_str}.{ext}"


aliyun_oss_service = AliyunOSSService()
