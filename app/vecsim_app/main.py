import uvicorn
from fastapi import FastAPI
from aredis_om import get_redis_connection, Migrator

from vecsim_app import config
from vecsim_app.schema import Product
from vecsim_app.api import routes

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/docs",
    openapi_url="/api"
)

# Routers
app.include_router(
    routes.product_router,
    prefix=config.API_V1_STR + "/product",
    tags=["products"],
)

@app.on_event("startup")
async def startup():
    # You can set the Redis OM URL using the REDIS_OM_URL environment
    # variable, or by manually creating the connection using your model's
    # Meta object.
    Product.Meta.database = get_redis_connection(url=config.REDIS_DATA_URL,
                                                  decode_responses=True)

    await Migrator().run()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
