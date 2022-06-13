import typing as t
import numpy as np
from fastapi import APIRouter
from redis import Redis
from vecsim_app.schema import Product, SimilarityRequest
from vecsim_app.query import create_query

product_router = r = APIRouter()

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
       redis_client = Redis(host="redis", port=6379, db=0)

       # find the vector of the Product listed in the request
       product_vector_key = "product_vector:" + str(similarity_request.product_id)
       vector = redis_client.hget(product_vector_key, "img_vector")

       # obtain results of the query
       results = redis_client.ft().search(q, query_params={"vec_param": vector})

       # Get Product records of those results
       similar_product_pks = [p.product_pk for p in results.docs]
       similar_products = [await Product.get(pk) for pk in similar_product_pks]
       return similar_products

