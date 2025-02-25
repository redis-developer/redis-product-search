from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

from productsearch import config
from productsearch.api.main import api_router
from productsearch.spa import SinglePageApplication
from productsearch.db.redis_helpers import get_async_index


@asynccontextmanager
async def lifespan(app: FastAPI):
    index = await get_async_index()
    async with index:
        yield


app = FastAPI(
    title=config.PROJECT_NAME, docs_url=config.API_DOCS, openapi_url=config.OPENAPI_DOCS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(api_router, prefix=config.API_V1_STR)

# static image files
app.mount("/data", StaticFiles(directory="data"), name="data")

## mount the built GUI react files into the static dir to be served.
current_file = Path(__file__)
project_root = current_file.parent.resolve()
frontend_build_dir = project_root / "templates" / "build"
app.mount(path="/", app=SinglePageApplication(directory=frontend_build_dir), name="SPA")


def main():
    server_attr = {"host": "0.0.0.0", "reload": True, "port": 8888, "workers": 1}
    if config.DEPLOYMENT_ENV == "prod":
        server_attr.update(
            {
                "reload": False,
                "workers": 2,
                "ssl_keyfile": "key.pem",
                "ssl_certfile": "full.pem",
            }
        )

    uvicorn.run("productsearch.main:app", **server_attr)


if __name__ == "__main__":
    main()
