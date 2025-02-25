import logging
import os

from fastapi import Request
from redisvl.index import AsyncSearchIndex
from redisvl.schema import IndexSchema

logger = logging.getLogger(__name__)


def get_schema() -> IndexSchema:
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/schema"
    file_path = os.path.join(dir_path, "products.yml")
    return IndexSchema.from_yaml(file_path)


def get_async_index(request: Request) -> AsyncSearchIndex:
    return request.app.state.redis_index
