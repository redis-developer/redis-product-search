
import redis.asyncio as redis

from vecsim_app import config


async def get_current_user_count():
    # TODO - feels like this should live somewhere else
    redis_conn = redis.from_url(config.REDIS_URL)
    count = await redis_conn.get('user_count')
    await redis_conn.incr('user_count')
    return count
