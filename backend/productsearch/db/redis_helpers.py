import logging
import os

from redisvl.index import AsyncSearchIndex, SearchIndex
from redisvl.schema import IndexSchema

from productsearch import config

logger = logging.getLogger(__name__)


dir_path = os.path.dirname(os.path.realpath(__file__)) + "/schema"
file_path = os.path.join(dir_path, "products.yml")
schema = IndexSchema.from_yaml(file_path)
_global_index = None


def get_test_index():
    index = SearchIndex.from_yaml(file_path, redis_url=config.REDIS_URL)

    if not index.exists():
        index.create(overwrite=True)

    return index


async def get_async_index():
    global _global_index
    if not _global_index:
        _global_index = AsyncSearchIndex(schema, redis_url=config.REDIS_URL)
    return _global_index
