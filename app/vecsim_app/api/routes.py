import random
import typing as t
from redis import Redis
from fastapi import APIRouter

from vecsim_app.schema import Product, ProductMetadata, SimilarityRequest, SearchRequest
from vecsim_app.query import create_query
from vecsim_app import config

product_router = r = APIRouter()

@r.get("/", response_model=t.List[Product],
       name="product:get_product_samples",
       operation_id="get_products_samples")
async def get_products(limit: int = 10, skip: int = 0):
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

@r.get("/{product_pk}",
       response_model=Product,
       name="product:get_metadata",
       operation_id="get_product_metadata")
async def get_product_metadata(product_pk: str):
    prod = await Product.get(product_pk)
    return Product.product_metadata

@r.get("/image/{product_pk}",
       name="product:get_image_url",
       operation_id="get_product_image_url")
async def get_product_image(product_pk: str):
    prod = await Product.get(product_pk)
    return prod.image_url

@r.post("/",
       name="product:create_product",
       operation_id="create_product")
async def create_product(product: Product):
    return await product.save()


@r.post("/bulk",
       name="product:bulk_create_product",
       operation_id="bulk_create_product")
async def bulk_create_product(products: t.List[Product]):
       for product in products:
              await product.save()

@r.put("/",
       response_model=t.List[Product],
       name="product:find_similar_products",
       operation_id="compute_similarity")
async def find_similar_products(similarity_request: SimilarityRequest) -> t.List[Product]:
       q = create_query(similarity_request.search_type,
                        similarity_request.number_of_results)

       #redis_client = Product.db()
       redis_client = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

       # find the vector of the Product listed in the request
       product_vector_key = "product_vector:" + str(similarity_request.product_id)
       vector = redis_client.hget(product_vector_key, "img_vector")

       # obtain results of the query
       results = redis_client.ft().search(q, query_params={"vec_param": vector})

       # Get Product records of those results
       similar_product_pks = [p.product_pk for p in results.docs]
       similar_products = [await Product.get(pk) for pk in similar_product_pks]
       return similar_products


@r.post("/search",
       response_model=t.List[Product],
       name="product:text_search",
       operation_id="text_search")
async def text_search_products(search: SearchRequest):
    products = await Product.find(
        Product.product_metadata.name % search.text).all()
    return products
