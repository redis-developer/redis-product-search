import typing as t
import redis.asyncio as redis

from fastapi import APIRouter
from vecsim_app import config
from vecsim_app import TEXT_MODEL
from vecsim_app.schema import (
    SimilarityRequest,
    SearchRequest,
    UserTextSimilarityRequest
)
from vecsim_app.models import Product
from vecsim_app.query import create_query


product_router = r = APIRouter()
redis_client = redis.from_url(config.REDIS_URL)

async def products_from_results(results) -> list:
    # extract products from VSS results
    return [await Product.get(p.product_pk) for p in results.docs]

@r.get("/", response_model=t.List[Product],
       name="product:get_product_samples",
       operation_id="get_products_samples")
async def get_products(limit: int = 20, skip: int = 0):
    pks = await Product.all_pks()
    if pks:
        # TODO figure out how to slice async_generator
        products = []
        i = 0
        async for pk in pks:
            if i >= skip and i < skip + limit:
                products.append(await Product.get(pk))
            if len(products) == limit:
                break
            i += 1
        return products
    return []


@r.post("/search",
       response_model=t.List[Product],
       name="product:text_search",
       operation_id="text_search")
async def text_search_products(search: SearchRequest):
    num_products = search.number_of_results
    products = await Product.find(
        Product.product_metadata.name % search.text).all()
    if len(products) > num_products:
        return products[:num_products]
    return products


@r.post("/vectorsearch/image",
       response_model=t.List[Product],
       name="product:find_similar_by_image",
       operation_id="compute_image_similarity")
async def find_products_by_image(similarity_request: SimilarityRequest) -> t.List[Product]:
    q = create_query(
        similarity_request.search_type,
        similarity_request.number_of_results,
        vector_field_name="img_vector",
        gender=similarity_request.gender,
        category=similarity_request.category
    )

    # find the vector of the Product listed in the request
    product_vector_key = "product_vector:" + str(similarity_request.product_id)
    vector = await redis_client.hget(product_vector_key, "img_vector")

    # obtain results of the query
    results = await redis_client.ft().search(q, query_params={"vec_param": vector})

    # Get Product records of those results
    similar_products = await products_from_results(results)
    return similar_products


@r.post("/vectorsearch/text",
       response_model=t.List[Product],
       name="product:find_similar_by_text",
       operation_id="compute_text_similarity")
async def find_products_by_text(similarity_request: SimilarityRequest) -> t.List[Product]:
    q = create_query(
        similarity_request.search_type,
        similarity_request.number_of_results,
        vector_field_name="text_vector",
        gender=similarity_request.gender,
        category=similarity_request.category
    )

    # find the vector of the Product listed in the request
    product_vector_key = "product_vector:" + str(similarity_request.product_id)
    vector = await redis_client.hget(product_vector_key, "text_vector")

    # obtain results of the query
    results = await redis_client.ft().search(q, query_params={"vec_param": vector})

    # Get Product records of those results
    similar_products = await products_from_results(results)
    return similar_products


@r.post("/vectorsearch/text/user",
       response_model=t.List[Product],
       name="product:find_similar_by_user_text",
       operation_id="compute_user_text_similarity")
async def find_products_by_user_text(similarity_request: UserTextSimilarityRequest) -> t.List[Product]:
    q = create_query(similarity_request.search_type,
                    similarity_request.number_of_results,
                    vector_field_name="text_vector",
                    gender=similarity_request.gender,
                    category=similarity_request.category)

    # obtain vector from text model in top level  __init__.py
    vector = TEXT_MODEL.encode(similarity_request.user_text)
    # obtain results of the query
    results = await redis_client.ft().search(q, query_params={"vec_param": vector.tobytes()})

    # Get Product records of those results
    similar_products = await products_from_results(results)
    return similar_products
