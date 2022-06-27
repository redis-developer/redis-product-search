import os

PROJECT_NAME = "vecsim_app"
API_DOCS = "/api/docs"
OPENAPI_DOCS = "/api/openapi.json"
REDIS_DATA_URL = os.environ.get("REDIS_DATA_URL", "redis://redis:6379")
REDIS_OM_URL = os.environ.get("REDIS_DATA_URL", "redis://redis:6379")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
API_V1_STR = "/api/v1"
DATA_LOCATION = os.environ.get("DATA_LOCATION", "../../data")
SUPERUSER_EMAIL = os.environ.get("SUPER_EMAIL", "s@p.com")
SUPERUSER_PASS = os.environ.get("SUPER_PASS", "secret")
SUPERUSER_FIRST = os.environ.get("SUPER_FIRST", "sam")
SUPERUSER_LAST = os.environ.get("SUPER_LAST", "lastname")

