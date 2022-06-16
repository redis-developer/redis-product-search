import uvicorn
from pathlib import Path
from aredis_om import get_redis_connection, Migrator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from vecsim_app import config
from vecsim_app.schema import Product
from vecsim_app.api import routes
from vecsim_app.spa import SinglePageApplication


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/docs",
    openapi_url="/api"
)

# dev only
app.add_middleware(
        CORSMiddleware,
        allow_origins="*", #   origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

# static files
app.mount("/static", StaticFiles(directory="static"), name="static")

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

# mount the built GUI react files into the static dir to be served.
#current_file = Path(__file__)
#project_root = current_file.parent.resolve()
#gui_build_dir = project_root / "templates" / "build"
#app.mount(
#    path="/", app=SinglePageApplication(directory=gui_build_dir), name="SPA"
#)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888)
