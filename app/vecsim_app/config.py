import os

PROJECT_NAME = "vecsim_app"
REDIS_DATA_URL = os.environ.get("REDIS_DATA_URL", "redis://redis:6379")
API_V1_STR = "/api/v1"
