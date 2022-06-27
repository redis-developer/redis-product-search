
import redis.asyncio as redis

from vecsim_app.config import REDIS_HOST, REDIS_PORT

# Dependency
def get_redis_client():
    client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT)
    try:
        yield client
    finally:
        client.close()


async def get_current_user_count():
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    count = await client.get('user_count')
    await client.incr('user_count')
    return count
