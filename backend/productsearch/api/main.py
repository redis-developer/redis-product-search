from fastapi import APIRouter

from productsearch.api.routes import product

api_router = APIRouter()
api_router.include_router(product.router, prefix="/product", tags=["product"])
