"""
Redis 连接
"""
import redis.asyncio as redis
from app.config import settings

redis_client: redis.Redis = None


async def init_redis():
    """初始化 Redis 连接"""
    global redis_client
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True
    )


async def close_redis():
    """关闭 Redis 连接"""
    global redis_client
    if redis_client:
        await redis_client.close()


async def get_redis() -> redis.Redis:
    """获取 Redis 客户端"""
    return redis_client