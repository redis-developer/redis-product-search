#!/usr/bin/env python3
import asyncio
import json
from typing import List

import numpy as np
import requests
from redisvl.index import AsyncSearchIndex

from productsearch import config
from productsearch.db.utils import get_schema


def read_from_s3():
    res = requests.get(config.S3_DATA_URL)
    return res.json()


def read_product_json_vectors() -> List:
    try:
        with open(config.DATA_LOCATION + "/products.json") as f:
            product_vectors = json.load(f)
    except FileNotFoundError:
        print("File not found, reading from S3")
        product_vectors = read_from_s3()

    return product_vectors


async def write_products(index: AsyncSearchIndex, products: List[dict]):
    """
    Write product records to Redis.

    Args:
        index (AsyncSearchIndex): Redis search index.
        products (list): List of documents to store.
    """

    def preprocess(product: dict) -> dict:
        return {
            "product_id": product["product_id"],
            # add tag fields to vectors for hybrid search
            "gender": product["product_metadata"]["gender"],
            "category": product["product_metadata"]["master_category"],
            # text fields
            "name": product["product_metadata"]["name"],
            "img_url": product["product_metadata"]["img_url"],
            # add image and text vectors as blobs
            "img_vector": np.array(product["img_vector"], dtype=np.float32).tobytes(),
            "text_vector": np.array(product["text_vector"], dtype=np.float32).tobytes(),
        }

    # TODO add an optional preprocessor callable to index.load()
    await index.load(
        data=[preprocess(product) for product in products],
        concurrency=config.WRITE_CONCURRENCY,
        id_field="product_id",
    )


async def load_data():
    schema = get_schema()
    index = AsyncSearchIndex(schema, redis_url=config.REDIS_URL)

    # Check if index exists
    if await index.exists() and len((await index.search("*")).docs) > 0:
        print("Index already exists and products ")
    else:
        # create a search index
        await index.create(overwrite=True)
        print("Loading products from file")
        products = read_product_json_vectors()
        print("Loading products into Redis")
        await write_products(index, products)
        print("Products successfully loaded")


if __name__ == "__main__":
    asyncio.run(load_data())
