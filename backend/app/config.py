"""
应用配置
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # 应用基础配置
    APP_NAME: str = "AI数字人视频定制平台"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # 服务地址
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/ai_digital_human?charset=utf8mb4"

    # Redis 配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # JWT 配置
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # OSS 配置
    QINIU_ACCESS_KEY: str = ""
    QINIU_SECRET_KEY: str = ""
    QINIU_BUCKET: str = ""
    QINIU_CDN_DOMAIN: str = ""

    # 短信配置
    ALIYUN_ACCESS_KEY: str = ""
    ALIYUN_SECRET_KEY: str = ""
    ALIYUN_SMS_SIGN_NAME: str = "AI数字人平台"
    ALIYUN_SMS_TEMPLATE_CODE: str = ""

    # 微信支付配置
    WECHAT_APP_ID: str = ""
    WECHAT_MCH_ID: str = ""
    WECHAT_API_KEY: str = ""
    WECHAT_CERT_PATH: str = ""
    WECHAT_KEY_PATH: str = ""

    # AI 服务配置
    AI_SERVICE_URL: str = ""
    AI_SERVICE_API_KEY: str = ""

    # 速率限制配置
    RATE_LIMIT_PER_MINUTE: int = 60

    # CORS 配置
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()