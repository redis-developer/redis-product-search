import os

S3_DATA_URL = "https://redis-product-search.s3.us-east-2.amazonaws.com/products.json"

RETURN_FIELDS = [
    "product_id",
    "name",
    "gender",
    "category",
    "img_url",
    "img_vector",
    "text_vector",
]

PROJECT_NAME = "productsearch"
API_DOCS = "/api/docs"
OPENAPI_DOCS = "/api/openapi.json"
INDEX_NAME = "products"
REDIS_HOST = os.environ.get("REDIS_HOST", "redis-vector-db")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
REDIS_DB = os.environ.get("REDIS_DB", 0)
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

API_V1_STR = "/api/v1"
DATA_LOCATION = os.environ.get("DATA_LOCATION", "../data")
DEPLOYMENT_ENV = os.environ.get("DEPLOYMENT", "dev")

WRITE_CONCURRENCY = os.environ.get("WRITE_CONCURRENCY", 150)
