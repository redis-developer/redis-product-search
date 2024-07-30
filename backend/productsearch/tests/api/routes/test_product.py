import pytest
from httpx import AsyncClient

from productsearch.main import app
from productsearch.api.schema.product import (
    SimilarityRequest,
)


@pytest.fixture
def gender(products):
    return products[0]["gender"]


@pytest.fixture
def category(products):
    return products[0]["category"]


@pytest.fixture
def bad_req_json():
    return {"not": "valid"}


@pytest.fixture
def product_req(gender, category, products):
    return SimilarityRequest(
        gender=gender,
        category=category,
        product_id=products[0]["product_id"],
    )


@pytest.mark.asyncio(scope="session")
async def test_root_w_filters(
    async_client: AsyncClient, gender: str, category: str
) -> None:

    response = await async_client.get(f"product/?gender={gender}&category={category}")

    assert response.status_code == 200
    content = response.json()

    assert content["total"] == 2
    assert len(content["products"]) == 2
    for p in content["products"]:
        assert p["category"] == category
        assert p["gender"] == gender


@pytest.mark.asyncio(scope="session")
async def test_root_na_category(async_client: AsyncClient, gender: str):

    response = await async_client.get(f"product/?gender={gender}&category=NA")

    assert response.status_code == 200
    content = response.json()
    assert content["total"] == 0
    assert len(content["products"]) == 0


@pytest.mark.asyncio(scope="session")
async def test_vector_by_text(
    async_client: AsyncClient,
    gender: str,
    category: str,
    product_req: SimilarityRequest,
):
    response = await async_client.post(
        f"product/vectorsearch/text", json=product_req.model_dump()
    )

    assert response.status_code == 200
    content = response.json()

    assert content["total"] == 2
    assert len(content["products"]) == 2
    for p in content["products"]:
        assert p["category"] == category
        assert p["gender"] == gender


@pytest.mark.asyncio(scope="session")
async def test_vector_by_text_bad_input(async_client: AsyncClient, bad_req_json: dict):

    response = await async_client.post(f"product/vectorsearch/text", json=bad_req_json)

    assert response.status_code == 422


@pytest.mark.asyncio(scope="session")
async def test_vector_by_img(
    async_client: AsyncClient,
    product_req: SimilarityRequest,
):
    response = await async_client.post(
        f"product/vectorsearch/image", json=product_req.model_dump()
    )

    assert response.status_code == 200
    content = response.json()

    assert content["total"] == 2
    assert len(content["products"]) == 2


@pytest.mark.asyncio(scope="session")
async def test_vector_by_img_bad_input(async_client: AsyncClient, bad_req_json: dict):

    response = await async_client.post(f"product/vectorsearch/image", json=bad_req_json)

    assert response.status_code == 422
