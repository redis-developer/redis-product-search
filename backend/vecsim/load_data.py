#!/usr/bin/env python3
import asyncio
import json
import numpy as np
import redis.asyncio as redis
import typing as t

from vecsim_app import config
from vecsim_app.models import Product
from vecsim_app.query import (
    create_flat_index,
    create_hnsw_index
)


def read_product_json() -> t.List:
    with open(config.DATA_LOCATION + "/product_metadata.json") as f:
        products = json.load(f)
    return products

def read_product_json_vectors() -> t.List:
    with open(config.DATA_LOCATION + "/product_vectors.json") as f:
        product_vectors = json.load(f)
    return product_vectors

async def gather_with_concurrency(n,  *products):
    semaphore = asyncio.Semaphore(n)
    with_pk = {}

    async def load_product(product):
        async with semaphore:
            nonlocal with_pk
            p = Product(**product)
            # use map to prevent sorting later
            with_pk[p.product_id] = p
            await p.save()

    await asyncio.gather(*[load_product(p) for p in products])
    return with_pk

async def set_product_vectors(product_vectors, redis_conn, products_with_pk):
    # iterate through products data and save vectors hash model
    for product in product_vectors:
        product_id = product["product_id"]
        product_pk = products_with_pk[product_id]
        key = "product_vector:" + str(product_id)
        await redis_conn.hset(
            key,
            mapping={
                "product_pk": product_pk.pk,
                "product_id": product_id,

                # Add tag fields to vectors for hybrid search
                "gender": product_pk.product_metadata.gender,
                "category": product_pk.product_metadata.master_category,

                # add image and text vectors as blobs
                "img_vector": np.array(product["img_vector"], dtype=np.float32).tobytes(),
                "text_vector": np.array(product["text_vector"], dtype=np.float32).tobytes()
        })

async def load_all_data():
    # TODO use redis-om connection
    redis_conn = redis.from_url(config.REDIS_URL)
    if await redis_conn.dbsize() > 5000:
        print("Products already loaded")
    else:
        print("Loading products into Vecsim App")
        products = read_product_json()
        products_with_pk = await gather_with_concurrency(100, *products)
        print("Products loaded!")

        print("Loading product vectors")
        vectors = read_product_json_vectors()
        await set_product_vectors(vectors, redis_conn, products_with_pk)
        print("Product vectors loaded!")

        print("Creating vector search index")
        # create a search index
        if config.INDEX_TYPE == "HNSW":
            await create_hnsw_index(redis_conn, len(products), prefix="product_vector:", distance_metric="COSINE")
        else:
            await create_flat_index(redis_conn, len(products), prefix="product_vector:", distance_metric="L2")
        print("Search index created")

if __name__ == "__main__":
    asyncio.run(load_all_data())
