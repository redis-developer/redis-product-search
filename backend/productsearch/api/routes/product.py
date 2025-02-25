import asyncio

import numpy as np
from fastapi import APIRouter, Depends, Request
from redis.commands.search.query import Query
from redisvl.index import AsyncSearchIndex
from redisvl.query import CountQuery, FilterQuery, VectorQuery
from redisvl.query.filter import FilterExpression, Tag

from productsearch import config
from productsearch.api.schema.product import (
    ProductSearchResponse,
    ProductVectorSearchResponse,
    SimilarityRequest,
)
from productsearch.db import utils

router = APIRouter()


@router.get(
    "/",
    response_model=ProductSearchResponse,
    name="product:get_product_samples",
    operation_id="get_products_samples",
)
async def get_products(
    request: Request,
    limit: int = 20,
    skip: int = 0,
    gender: str = "",
    category: str = "",
) -> ProductSearchResponse:
    """Fetch and return products based on gender and category fields

    Args:
        limit (int, optional): _description_. Defaults to 20.
        skip (int, optional): _description_. Defaults to 0.
        gender (str, optional): _description_. Defaults to "".
        category (str, optional): _description_. Defaults to "".

    Returns:
        ProductSearchResponse: Pydantic model containing products and total count
    """
    index = utils.get_async_index(request)

    # Build query
    filter_expression = (Tag("gender") == gender) & (Tag("category") == category)
    filter_query = FilterQuery(return_fields=[], filter_expression=filter_expression)
    # Execute search
    result_papers = await index.search(filter_query.query.paging(skip, limit))
    return ProductSearchResponse(
        total=result_papers.total, products=[d.__dict__ for d in result_papers.docs]
    )


@router.post(
    "/vectorsearch/image",
    response_model=ProductVectorSearchResponse,
    name="product:find_similar_by_image",
    operation_id="compute_image_similarity",
)
async def find_products_by_image(
    request: Request,
    similarity_request: SimilarityRequest,
) -> ProductVectorSearchResponse:
    """Fetch and return products based on image similarity

    Args:
        SimilarityRequest:
            number_of_results (int): Number of results to return
            search_type (str): Search type
            gender (str): filter criteria
            category (str): filter criteria

    Returns:
        ProductSearchResponse:
            total (int): Total number of results
            products (list[VectorSearchProduct]): List of products
                product_id (str): Product ID
                name (str): Product name
                gender (str): fashion tag
                category (str): fashion tag
                img_url (str): Image URL for displaying in FE
                text_vector (str): Text vector for similarity computation
                img_vector (str): Image vector for similarity computation
    """
    index = utils.get_async_index(request)

    # Fetch paper key and the vector from the HASH, cast to numpy array
    product = await index.fetch(similarity_request.product_id)
    product_img_vector = np.frombuffer(product["img_vector"], dtype=np.float32)

    # Build filter expression
    filter_expression = (Tag("gender") == similarity_request.gender) & (
        Tag("category") == similarity_request.category
    )

    # Create queries
    paper_similarity_query = VectorQuery(
        vector=product_img_vector,
        vector_field_name="img_vector",
        num_results=similarity_request.number_of_results,
        return_fields=config.RETURN_FIELDS,
        filter_expression=filter_expression,
    )
    count_query = CountQuery(filter_expression)

    # Execute search
    count, result_papers = await asyncio.gather(
        index.query(count_query), index.query(paper_similarity_query)
    )
    # Get Paper records of those results
    return ProductVectorSearchResponse(total=count, products=result_papers)


@router.post(
    "/vectorsearch/text",
    response_model=ProductVectorSearchResponse,
    name="product:find_similar_by_text",
    operation_id="compute_text_similarity",
)
async def find_products_by_text(
    request: Request,
    similarity_request: SimilarityRequest,
) -> ProductVectorSearchResponse:
    """Fetch and return products based on image similarity

    Args:
        SimilarityRequest:
            number_of_results (int): Number of results to return
            search_type (str): Search type
            gender (str): filter criteria
            category (str): filter criteria

    Returns:
        ProductSearchResponse:
            total (int): Total number of results
            products (list[VectorSearchProduct]): List of products
                product_id (str): Product ID
                name (str): Product name
                gender (str): fashion tag
                category (str): fashion tag
                img_url (str): Image URL for displaying in FE
                text_vector (str): Text vector for similarity computation
                img_vector (str): Image vector for similarity computation
    """
    index = utils.get_async_index(request)

    # Fetch paper key and the vector from the HASH, cast to numpy array
    product = await index.fetch(similarity_request.product_id)
    product_text_vector = np.frombuffer(product["text_vector"], dtype=np.float32)

    # Build filter expression
    filter_expression = (Tag("gender") == similarity_request.gender) & (
        Tag("category") == similarity_request.category
    )

    # Create queries
    paper_similarity_query = VectorQuery(
        vector=product_text_vector,
        vector_field_name="text_vector",
        num_results=similarity_request.number_of_results,
        return_fields=config.RETURN_FIELDS,
        filter_expression=filter_expression,
    )
    count_query = CountQuery(filter_expression)

    # Execute search
    count, result_papers = await asyncio.gather(
        index.query(count_query), index.query(paper_similarity_query)
    )
    # Get Paper records of those results
    return ProductVectorSearchResponse(total=count, products=result_papers)
