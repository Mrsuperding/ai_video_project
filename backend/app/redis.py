"""
Redis 连接
"""
import redis.asyncio as redis
import redis as sync_redis
from app.config import settings

redis_client: redis.Redis = None
sync_redis_client: sync_redis.Redis = None


async def init_redis():
    """初始化 Redis 连接"""
    global redis_client, sync_redis_client
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True
    )
    sync_redis_client = sync_redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        decode_responses=True
    )


async def close_redis():
    """关闭 Redis 连接"""
    global redis_client, sync_redis_client
    if redis_client:
        await redis_client.close()
    if sync_redis_client:
        sync_redis_client.close()


def get_sync_redis() -> sync_redis.Redis:
    """获取同步 Redis 客户端"""
    return sync_redis_client


async def get_redis() -> redis.Redis:
    """获取异步 Redis 客户端"""
    return redis_client