#!/usr/bin/env python3
import typing as t
import json
import asyncio
import numpy as np

from redis import Redis

from vecsim_app.query import create_flat_index
from vecsim_app.schema import Product
from vecsim_app import config

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
    with_pk = []

    async def load_product(product):
        async with semaphore:
            nonlocal with_pk
            p = Product(**product)
            with_pk.append(p)
            await p.save()

    await asyncio.gather(*[load_product(p) for p in products])
    return with_pk

def set_product_vectors(product_vectors, redis_conn, products_with_pk):
    # sort products with pk by value of product_id
    products_with_pk.sort(key=lambda x: x.product_id)
    product_vectors.sort(key=lambda x: x["product_id"])

    for product, product_pk in zip(product_vectors, products_with_pk):
        key = "product_vector:" + str(product["product_id"])
        redis_conn.hset(key,
                        mapping={
                            "product_pk": product_pk.pk,
                            "product_id": product["product_id"],
                            "img_vector": np.array(product["img_vector"], dtype=np.float32).tobytes(),
                            "text_vector": np.array(product["text_vector"], dtype=np.float32).tobytes()
                            })


async def load_all_data():
    print("Loading products into Vecsim App")
    products = read_product_json()
    products_with_pk = await gather_with_concurrency(1000, *products)
    print("Products loaded!")

    # TODO use redis-om connection
    redis_conn = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

    print("loading product vectors")
    vectors = read_product_json_vectors()
    set_product_vectors(vectors, redis_conn, products_with_pk)
    print("product vectors loaded!")

    print("Creating vector search index")
    # create a search index
    create_flat_index(redis_conn, len(products))
    print("Search index created")


if __name__ == "__main__":
    asyncio.run(load_all_data())
