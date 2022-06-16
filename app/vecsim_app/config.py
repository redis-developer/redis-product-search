import os

PROJECT_NAME = "vecsim_app"
REDIS_DATA_URL = os.environ.get("REDIS_DATA_URL", "redis://redis:6379")
REDIS_OM_URL = os.environ.get("REDIS_DATA_URL", "redis://redis:6379")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
API_V1_STR = "/api/v1"
DATA_LOCATION = os.environ.get("DATA_LOCATION", "../../data")


