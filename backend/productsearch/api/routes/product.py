import asyncio
from typing import Any, Dict, List, Union

import numpy as np
from fastapi import APIRouter, Depends
from redis.commands.search.document import Document
from redis.commands.search.query import Query
from redis.commands.search.result import Result
from redisvl.index import AsyncSearchIndex
from redisvl.query import FilterQuery, VectorQuery
from redisvl.query.filter import FilterExpression, Tag

from productsearch import TEXT_MODEL, config
from productsearch.api.schema.product import (
    ProductSearchResponse,
    ProductVectorSearchResponse,
    SimilarityRequest,
    UserTextSimilarityRequest,
)
from productsearch.db import redis_helpers

router = APIRouter()


# def process_product(product: Union[Document, Dict[str, Any]]) -> Dict[str, Any]:
#     """
#     Process product data and calculate similarity score.

#     Args:
#         product: Input product data.

#     Returns:
#         dict: Processed product data with similarity score.
#     """
#     if not isinstance(product, dict):
#         product = product.__dict__
#     if "vector_distance" in product:
#         product["similarity_score"] = 1 - float(product["vector_distance"])
#     return product


# def prepare_response(
#     total: int, results: Union[List[Dict[str, Any]], Result]
# ) -> Dict[str, Any]:
#     """
#     Extract and process products from search results.

#     This function extracts products from the provided search results, processes each paper,
#     and returns a dictionary containing the total count and a list of processed papers.

#     Args:
#         total (int): The hypothetical count of papers present in the db that match the filters.
#         results (list): The iterable containing raw paper data.

#     Returns:
#         dict: A dictionary with 'total' count and a list of 'papers', where each paper is a processed dict.
#     """
#     # extract papers from VSS results
#     if not isinstance(results, list):
#         results = results.docs
#     return {"total": total, "papers": [process_product(product) for product in results]}


def create_count_query(filter_expression: FilterExpression) -> Query:
    """
    Create a "count" query where simply want to know how many records
    match a particular filter expression

    Args:
        filter_expression (FilterExpression): The filter expression for the query.

    Returns:
        Query: The Redis query object.
    """
    return Query(str(filter_expression)).no_content().dialect(2)


@router.get(
    "/",
    response_model=ProductSearchResponse,
    name="product:get_product_samples",
    operation_id="get_products_samples",
)
async def get_products(
    limit: int = 20,
    skip: int = 0,
    gender: str = "",
    category: str = "",
    index: AsyncSearchIndex = Depends(redis_helpers.get_async_index),
):
    """_summary_

    Args:
        limit (int, optional): _description_. Defaults to 20.
        skip (int, optional): _description_. Defaults to 0.
        gender (str, optional): _description_. Defaults to "".
        category (str, optional): _description_. Defaults to "".

    Returns:
        ProductSearchResponse model
    """
    # Build query
    filter_expression = (Tag("gender") == gender) & (Tag("category") == category)
    filter_query = FilterQuery(return_fields=[], filter_expression=filter_expression)
    # Execute search
    result_papers = await index.search(filter_query.query.paging(skip, limit))
    # return prepare_response(result_papers.total, result_papers)
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
    similarity_request: SimilarityRequest,
    index: AsyncSearchIndex = Depends(redis_helpers.get_async_index),
) -> ProductVectorSearchResponse:

    # Fetch paper key and the vector from the HASH, cast to numpy array
    product_key = f"{index.schema.index.prefix}:{similarity_request.product_id}"
    product_img_vector = np.frombuffer(
        await index.client.hget(product_key, "img_vector"), dtype=np.float32
    )

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
    count_query = create_count_query(filter_expression)

    # Execute search
    count, result_papers = await asyncio.gather(
        index.search(count_query), index.query(paper_similarity_query)
    )
    # Get Paper records of those results
    return ProductVectorSearchResponse(total=count.total, products=result_papers)


@router.post(
    "/vectorsearch/text",
    response_model=ProductVectorSearchResponse,
    name="product:find_similar_by_text",
    operation_id="compute_text_similarity",
)
async def find_products_by_text(
    similarity_request: SimilarityRequest,
    index: AsyncSearchIndex = Depends(redis_helpers.get_async_index),
) -> ProductVectorSearchResponse:
    # Fetch paper key and the vector from the HASH, cast to numpy array
    product_key = f"{index.schema.index.prefix}:{similarity_request.product_id}"
    product_text_vector = np.frombuffer(
        await index.client.hget(product_key, "text_vector"), dtype=np.float32
    )

    # Build filter expression
    filter_expression = (Tag("gender") == similarity_request.gender) & (
        Tag("category") == similarity_request.category
    )

    # Create queries
    paper_similarity_query = VectorQuery(
        vector=product_text_vector,
        vector_field_name="text_vector",
        num_results=similarity_request.number_of_results,
        return_fields=config.RETURN_FIELDS,  # TODO: I don't think it makes sense to have return fields specified by FE => modify request schema => move to config
        filter_expression=filter_expression,
    )
    count_query = create_count_query(filter_expression)

    # Execute search
    count, result_papers = await asyncio.gather(
        index.search(count_query), index.query(paper_similarity_query)
    )
    # Get Paper records of those results
    return ProductVectorSearchResponse(total=count.total, products=result_papers)
