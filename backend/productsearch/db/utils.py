import logging
import os

from redisvl.index import AsyncSearchIndex
from redisvl.schema import IndexSchema

from productsearch import config

logger = logging.getLogger(__name__)

# global search index
_global_index = None


def get_schema() -> IndexSchema:
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/schema"
    file_path = os.path.join(dir_path, "products.yml")
    return IndexSchema.from_yaml(file_path)


async def get_async_index():
    global _global_index
    if not _global_index:
        _global_index = AsyncSearchIndex(get_schema(), redis_url=config.REDIS_URL)
    return _global_index
