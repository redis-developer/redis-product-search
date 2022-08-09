import uvicorn
from pathlib import Path
from aredis_om import get_redis_connection, Migrator

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from vecsim_app import config
from vecsim_app.models import Product
from vecsim_app.api import routes, user_routes, auth_routes
from vecsim_app.spa import SinglePageApplication
from vecsim_app.auth import (
    get_current_active_user,
    get_current_active_superuser
)


app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url=config.API_DOCS,
    openapi_url=config.OPENAPI_DOCS
)

app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

# Routers
app.include_router(auth_routes.auth_router, prefix="/api", tags=["auth"])
app.include_router(
    routes.product_router,
    prefix=config.API_V1_STR + "/product",
    tags=["products"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(
    user_routes.users_router,
    prefix=config.API_V1_STR,
    tags=["users"],
    dependencies=[Depends(get_current_active_superuser)]
)


@app.on_event("startup")
async def startup():
    # You can set the Redis OM URL using the REDIS_OM_URL environment
    # variable, or by manually creating the connection using your model's
    # Meta object.
    Product.Meta.database = get_redis_connection(url=config.REDIS_DATA_URL,
                                                 decode_responses=True)

    await Migrator().run()

# static image files
app.mount("/data", StaticFiles(directory="data"), name="data")

## mount the built GUI react files into the static dir to be served.
current_file = Path(__file__)
project_root = current_file.parent.resolve()
gui_build_dir = project_root / "templates" / "build"
app.mount(
    path="/", app=SinglePageApplication(directory=gui_build_dir), name="SPA"
)


if __name__ == "__main__":
    import os
    env = os.environ.get("DEPLOYMENT", "prod")

    server_attr = {
        "host": "0.0.0.0",
        "reload": True,
        "port": 8888,
        "workers": 1
    }
    if env == "prod":
        server_attr.update({"reload": False,
                            "workers": 3,
                            "ssl_keyfile": "certs/key.pem", # replaced
                            "ssl_certfile": "certs/cert.pem"})

    uvicorn.run("main:app", **server_attr)
