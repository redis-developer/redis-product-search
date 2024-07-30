import logging
import os
from typing import List

from redis.asyncio import Redis
from redisvl.index import AsyncSearchIndex, SearchIndex
from redisvl.query.filter import FilterExpression, Tag
from redisvl.schema import IndexSchema

from productsearch import config

logger = logging.getLogger(__name__)


dir_path = os.path.dirname(os.path.realpath(__file__)) + "/schema"
schema = IndexSchema.from_yaml(os.path.join(dir_path, "products.yml"))
client = Redis.from_url(config.REDIS_URL)
global_index = None


async def get_async_index():
    global global_index
    if not global_index:
        global_index = AsyncSearchIndex(schema, client)
    yield global_index
