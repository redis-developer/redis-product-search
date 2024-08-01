from asyncio import get_event_loop
from typing import Generator

import pytest
import pytest_asyncio
from httpx import AsyncClient
from redis.asyncio import Redis

from productsearch import config
from productsearch.main import app
from productsearch.tests.utils.seed import seed_test_db


@pytest.fixture(scope="module")
def products():
    products = seed_test_db()
    return products


@pytest.fixture
async def client():
    client = await Redis.from_url(config.REDIS_URL)
    yield client
    try:
        await client.aclose()
    except RuntimeError as e:
        if "Event loop is closed" not in str(e):
            raise


@pytest_asyncio.fixture(scope="session")
async def async_client():

    async with AsyncClient(app=app, base_url="http://test/api/v1/") as client:

        yield client
