"""
安全工具 - JWT、密码哈希、数据加密
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import base64
import hashlib
from app.config import settings

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 敏感数据加密
_encryption_key = None


def _get_encryption_key() -> bytes:
    """获取加密密钥（基于 SECRET_KEY 派生）"""
    global _encryption_key
    if _encryption_key is None:
        key = hashlib.sha256(SECRET_KEY.encode()).digest()
        _encryption_key = base64.urlsafe_b64encode(key)
    return _encryption_key


def get_cipher() -> Fernet:
    """获取 Fernet 加密器"""
    return Fernet(_get_encryption_key())


def encrypt_data(data: str) -> str:
    """加密敏感数据（如身份证号）"""
    if not data:
        return data
    cipher = get_cipher()
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()


def decrypt_data(encrypted_data: str) -> str:
    """解密敏感数据"""
    if not encrypted_data:
        return encrypted_data
    cipher = get_cipher()
    decrypted = cipher.decrypt(encrypted_data.encode())
    return decrypted.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """哈希密码"""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "type": "access",
        "iat": datetime.utcnow()
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """创建刷新令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "iat": datetime.utcnow()
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """解码令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def create_tokens(user_id: int, role: str = "user") -> Dict[str, str]:
    """创建用户令牌对

    Args:
        user_id: 用户ID
        role: 角色类型，"user" 或 "admin"
    """
    access_token = create_access_token({
        "user_id": user_id,
        "role": role
    })
    refresh_token = create_refresh_token({
        "user_id": user_id
    })
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "token_type": "Bearer"
    }