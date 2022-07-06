import random
import typing as t
from redis.asyncio import Redis
from fastapi import APIRouter, Depends

from vecsim_app.schema import SimilarityRequest, SearchRequest, UserTextSimilarityRequest
from vecsim_app.models import Product
from vecsim_app.query import create_query
from vecsim_app import config
from vecsim_app import TEXT_MODEL

product_router = r = APIRouter()

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
    q = create_query(similarity_request.search_type,
                    similarity_request.number_of_results,
                    vector_field_name="img_vector",
                    gender=similarity_request.gender,
                    category=similarity_request.category)

    redis_client = await Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

    # find the vector of the Product listed in the request
    product_vector_key = "product_vector:" + str(similarity_request.product_id)
    vector = await redis_client.hget(product_vector_key, "img_vector")

    # obtain results of the query
    results = await redis_client.ft().search(q, query_params={"vec_param": vector})

    # Get Product records of those results
    similar_product_pks = [p.product_pk for p in results.docs]
    similar_products = [await Product.get(pk) for pk in similar_product_pks]
    return similar_products


@r.post("/vectorsearch/text",
       response_model=t.List[Product],
       name="product:find_similar_by_text",
       operation_id="compute_text_similarity")
async def find_products_by_text(similarity_request: SimilarityRequest) -> t.List[Product]:
    q = create_query(similarity_request.search_type,
                    similarity_request.number_of_results,
                    vector_field_name="text_vector",
                    gender=similarity_request.gender,
                    category=similarity_request.category)

    redis_client = await Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

    # find the vector of the Product listed in the request
    product_vector_key = "product_vector:" + str(similarity_request.product_id)
    vector = await redis_client.hget(product_vector_key, "text_vector")

    # obtain results of the query
    results = await redis_client.ft().search(q, query_params={"vec_param": vector})

    # Get Product records of those results
    similar_product_pks = [p.product_pk for p in results.docs]
    similar_products = [await Product.get(pk) for pk in similar_product_pks]
    return similar_products


@r.post("/vectorsearch/text/user",
       response_model=t.List[Product],
       name="product:find_similar_by_user_text",
       operation_id="compute_user_text_similarity")
async def find_products_by_user_text(similarity_request: UserTextSimilarityRequest) -> t.List[Product]:
    q = create_query(similarity_request.search_type,
                    similarity_request.number_of_results,
                    vector_field_name="text_vector")

    redis_client = await Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

    # obtain vector from text model in top level  __init__.py
    vector = TEXT_MODEL.encode(similarity_request.user_text)
    # obtain results of the query
    results = await redis_client.ft().search(q, query_params={"vec_param": vector.tobytes()})

    # Get Product records of those results
    similar_product_pks = [p.product_pk for p in results.docs]
    similar_products = [await Product.get(pk) for pk in similar_product_pks]
    return similar_products

