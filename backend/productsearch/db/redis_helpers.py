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
file_path = os.path.join(dir_path, "products.yml")
schema = IndexSchema.from_yaml(file_path)
client = Redis.from_url(config.REDIS_URL)
global_index = None


def get_test_index():
    index = SearchIndex.from_yaml(file_path)
    index.connect(redis_url=config.REDIS_URL)

    if not index.exists():
        index.create(overwrite=True)

    return index


async def get_async_index():
    global global_index
    if not global_index:
        global_index = AsyncSearchIndex(schema, client)
    yield global_index
