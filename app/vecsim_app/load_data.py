#!/usr/bin/env python3
import typing as t
import json
import asyncio
import numpy as np

from vecsim_app.query import create_flat_index, create_hnsw_index
from vecsim_app.models import Product, ProductVectors
from vecsim_app.schema import UserCreate
from vecsim_app.crud import create_user
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

async def set_user_count(redis_conn):
    await redis_conn.set("user_count", 0)

async def set_superuser_account():
    user_dict = {
        "email": config.SUPERUSER_EMAIL,
        "password": config.SUPERUSER_PASS,
        "is_active": True,
        "is_superuser": True,
        "first_name": config.SUPERUSER_FIRST,
        "last_name": config.SUPERUSER_LAST,
        "title": "Principal Engineer",
        "company": "Redis"
    }
    superuser = UserCreate(**user_dict)
    await create_user(superuser)

async def set_product_vectors(product_vectors, products_with_pk):
    # iterate through products data and save vectors hash model
    for product in product_vectors:
        product_id = product["product_id"]
        product_pk = products_with_pk[product_id]
        product_vectors = ProductVectors(
            product_id=product_id,
            gender=product_pk.product_metadata.gender,
            category=product_pk.product_metadata.master_category,
            img_vector=np.array(product["img_vector"], dtype=np.float32).tobytes(),
            text_vector=np.array(product["text_vector"], dtype=np.float32).tobytes()
        )
        await product_vectors.save()

async def load_all_data():
    redis_conn = ProductVectors.db()
    keys = await redis_conn.keys()
    if len(keys) > 10000:
        print("Products already loaded")
    else:
        print("Loading products into Vecsim App")
        products = read_product_json()
        products_with_pk = await gather_with_concurrency(100, *products)
        print("Products loaded!")

        print("Loading product vectors")
        vectors = read_product_json_vectors()
        await set_product_vectors(vectors, products_with_pk)
        print("Product vectors loaded!")

        print("Creating vector search index")
        # create a search index
        if config.INDEX_TYPE == "HNSW":
            await create_hnsw_index(redis_conn, len(products), distance_metric="COSINE")
        else:
            await create_flat_index(redis_conn, len(products), distance_metric="L2")
        print("Search index created")

    if not await redis_conn.exists("user_count"):
        await set_user_count(redis_conn)

        print("Creating Superuser")
        await set_superuser_account()
        print("Created superuser")

if __name__ == "__main__":
    asyncio.run(load_all_data())
