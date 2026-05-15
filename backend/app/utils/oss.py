"""
OSS Utilities - Qiniu Cloud Storage
"""
import base64
import hashlib
import time
from typing import Optional

import qiniu.config
from qiniu import Auth, BucketManager

from app.config import settings


class OSSService:
    """Qiniu OSS service"""

    def __init__(self):
        self.auth = None
        self.bucket_manager = None
        if settings.QINIU_ACCESS_KEY and settings.QINIU_SECRET_KEY:
            self.auth = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
            self.bucket_manager = BucketManager(self.auth)

    def generate_upload_token(self, key: str, expires: int = 3600) -> Optional[str]:
        """Generate upload token"""
        if not self.auth:
            return None
        return self.auth.upload_token(settings.QINIU_BUCKET, key, expires)

    def generate_download_url(self, key: str, expires: int = 3600) -> Optional[str]:
        """Generate download URL"""
        if not self.auth:
            return None
        base_url = f"{settings.QINIU_CDN_DOMAIN}/{key}"
        return self.auth.private_download_url(base_url, expires)

    def upload_file(self, local_file: str, key: str) -> bool:
        """Upload file to OSS"""
        import qiniu.io
        if not self.auth:
            return False
        token = self.generate_upload_token(key)
        if not token:
            return False
        try:
            ret, err = qiniu.io.put_file(token, key, local_file)
            return err is None
        except Exception:
            return False

    def delete_file(self, key: str) -> bool:
        """Delete file from OSS"""
        if not self.bucket_manager:
            return False
        try:
            ret, err = self.bucket_manager.delete(settings.QINIU_BUCKET, key)
            return err is None
        except Exception:
            return False

    def get_file_info(self, key: str) -> Optional[dict]:
        """Get file info"""
        if not self.bucket_manager:
            return None
        try:
            ret, err = self.bucket_manager.stat(settings.QINIU_BUCKET, key)
            if err is None:
                return {
                    "size": ret.get("fsize"),
                    "mime_type": ret.get("mimeType"),
                    "hash": ret.get("hash"),
                    "put_time": ret.get("putTime")
                }
        except Exception:
            pass
        return None

    @staticmethod
    def generate_key(filename: str, prefix: str = "") -> str:
        """Generate unique file key"""
        timestamp = int(time.time() * 1000)
        ext = filename.split(".")[-1] if "." in filename else ""
        hash_str = hashlib.md5(f"{filename}{timestamp}".encode()).hexdigest()[:8]
        if prefix:
            return f"{prefix}/{timestamp}_{hash_str}.{ext}"
        return f"{timestamp}_{hash_str}.{ext}"


oss_service = OSSService()