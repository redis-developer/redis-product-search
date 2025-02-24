import logging
import os

from redis.asyncio import Redis
from redisvl.index import AsyncSearchIndex, SearchIndex
from redisvl.schema import IndexSchema

from productsearch import config

logger = logging.getLogger(__name__)


dir_path = os.path.dirname(os.path.realpath(__file__)) + "/schema"
file_path = os.path.join(dir_path, "products.yml")
schema = IndexSchema.from_yaml(file_path)
global_index = None


def get_test_index():
    index = SearchIndex.from_yaml(file_path, redis_url=config.REDIS_URL)

    if not index.exists():
        index.create(overwrite=True)

    return index


async def get_async_index():
    global global_index
    if not global_index:
        global_index = AsyncSearchIndex(schema, redis_url=config.REDIS_URL)
    yield global_index
