import json
import os

import httpx
import numpy as np
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from redisvl.index import SearchIndex

from productsearch import config
from productsearch.db.utils import get_schema
from productsearch.main import app


@pytest_asyncio.fixture(scope="session")
def index():
    index = SearchIndex(schema=get_schema(), redis_url=config.REDIS_URL)
    index.create()
    yield index
    index.disconnect()


@pytest.fixture(scope="session", autouse=True)
def test_data(index):
    cwd = os.getcwd()
    with open(f"{cwd}/productsearch/tests/test_vectors.json", "r") as f:
        products = json.load(f)

    parsed_products = []

    # convert to bytes
    for product in products:
        parsed = {}
        parsed["text_vector"] = np.array(
            product["text_vector"], dtype=np.float32
        ).tobytes()
        parsed["img_vector"] = np.array(
            product["img_vector"], dtype=np.float32
        ).tobytes()
        parsed["category"] = product["product_metadata"]["master_category"]
        parsed["img_url"] = product["product_metadata"]["img_url"]
        parsed["name"] = product["product_metadata"]["name"]
        parsed["gender"] = product["product_metadata"]["gender"]
        parsed["product_id"] = product["product_id"]
        parsed_products.append(parsed)

    keys = index.load(data=parsed_products, id_field="product_id")
    return parsed_products


@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with LifespanManager(app):
        async with AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test/api/v1/"
        ) as client:
            yield client
