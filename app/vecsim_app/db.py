
import redis.asyncio as redis

from vecsim_app import config

# Dependency
def get_redis_client():
    client = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD,
        db=0)
    try:
        yield client
    finally:
        client.close()


async def get_current_user_count():
    with get_redis_client() as client:
        count = await client.get('user_count')
        await client.incr('user_count')
        return count
