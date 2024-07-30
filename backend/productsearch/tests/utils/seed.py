import json
import os

import numpy as np

from productsearch.db import redis_helpers


def seed_test_db():
    cwd = os.getcwd()
    with open(f"{cwd}/productsearch/tests/utils/test_vectors.json", "r") as f:
        products = json.load(f)

    parsed_products = []

    # convert to bytes
    for product in products:
        parsed = {}
        parsed["text_vector"] = np.array(
            product["text_vector"], dtype=np.float32
        ).tobytes()
        parsed["img_vector"] = np.array(
            product["img_vector"], dtype=np.float32
        ).tobytes()
        parsed["category"] = product["product_metadata"]["master_category"]
        parsed["img_url"] = product["product_metadata"]["img_url"]
        parsed["name"] = product["product_metadata"]["name"]
        parsed["gender"] = product["product_metadata"]["gender"]
        parsed["product_id"] = product["product_id"]
        parsed_products.append(parsed)

    index = redis_helpers.get_test_index()
    index.load(data=parsed_products, id_field="product_id")
    return parsed_products
