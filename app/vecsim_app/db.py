
import redis.asyncio as redis

from vecsim_app import config


async def get_current_user_count():
    # TODO - feels like this should live somewhere else
    redis_conn = redis.Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD,
        db=0
    )
    count = await redis_conn.get('user_count')
    await redis_conn.incr('user_count')
    return count
