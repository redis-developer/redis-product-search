import asyncio
import numpy as np

from redis.commands.search.query import Query
from redis.commands.search.document import Document
from redis.commands.search.result import Result

from redisvl.index import AsyncSearchIndex
from redisvl.query import VectorQuery, FilterQuery
from redisvl.query.filter import Tag, FilterExpression
from fastapi import APIRouter

from productsearch import config
from productsearch import TEXT_MODEL
from productsearch.schema import (
    SimilarityRequest,
    UserTextSimilarityRequest
)
from vecsim_app.models import Product
from vecsim_app.query import create_query, count

from typing import List, Dict, Any, Union


product_router = r = APIRouter()

def process_product(product: Union[Document, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Process product data and calculate similarity score.

    Args:
        product: Input product data.

    Returns:
        dict: Processed product data with similarity score.
    """
    if not isinstance(product, dict):
        product = product.__dict__
    if 'vector_distance' in product:
        product['similarity_score'] = 1 - float(product['vector_distance'])
    return product

def prepare_response(total: int, results: Union[List[Dict[str, Any]], Result]) -> Dict[str, Any]:
    """
    Extract and process products from search results.

    This function extracts products from the provided search results, processes each paper,
    and returns a dictionary containing the total count and a list of processed papers.

    Args:
        total (int): The hypothetical count of papers present in the db that match the filters.
        results (list): The iterable containing raw paper data.

    Returns:
        dict: A dictionary with 'total' count and a list of 'papers', where each paper is a processed dict.
    """
    # extract papers from VSS results
    if not isinstance(results, list):
        results = results.docs
    return {
        'total': total,
        'papers': [process_product(product) for product in results]
    }


def create_count_query(filter_expression: FilterExpression) -> Query:
    """
    Create a "count" query where simply want to know how many records
    match a particular filter expression

    Args:
        filter_expression (FilterExpression): The filter expression for the query.

    Returns:
        Query: The Redis query object.
    """
    return (
        Query(str(filter_expression))
        .no_content()
        .dialect(2)
    )

@r.get("/", response_model=Dict,
       name="product:get_product_samples",
       operation_id="get_products_samples")
async def get_products(
    limit: int = 20,
    skip: int = 0,
    gender: str = "",
    category: str = ""
):
    """_summary_

    Args:
        limit (int, optional): _description_. Defaults to 20.
        skip (int, optional): _description_. Defaults to 0.
        gender (str, optional): _description_. Defaults to "".
        category (str, optional): _description_. Defaults to "".

    Returns:
        _type_: _description_
    """
    index = await AsyncSearchIndex.from_existing(
        name=config.INDEX_NAME,
        url=config.REDIS_URL
    )
    # Build query
    filter_expression = (Tag("gender") == gender) & (Tag("category") == category)
    filter_query = FilterQuery(
        return_fields=[], filter_expression=filter_expression)
    # Execute search
    result_papers = await index.search(
        filter_query.query.paging(skip, limit)
    )
    return prepare_response(result_papers.total, result_papers)


# @r.post("/search",
#        response_model=t.List[Product],
#        name="product:text_search",
#        operation_id="text_search")
# async def text_search_products(search: SearchRequest):
#     num_products = search.number_of_results
#     products = await Product.find(
#         Product.product_metadata.name % search.text
#     ).copy(offset=0, limit=num_products).execute()
#     return products


@r.post("/vectorsearch/image",
       response_model=Dict,
       name="product:find_similar_by_image",
       operation_id="compute_image_similarity")
async def find_products_by_image(similarity_request: SimilarityRequest) -> Dict:
    index = await AsyncSearchIndex.from_existing(
        name=config.INDEX_NAME,
        url=config.REDIS_URL
    )
    # Fetch paper key and the vector from the HASH, cast to numpy array
    product_key = index._get_key({"product_id": similarity_request.product_id}, "product_id")
    product_img_vector = np.frombuffer(
        await index.client.hget(product_key, "img_vector"),
        dtype=np.float32
    )

    # Build filter expression
    filter_expression = (Tag("gender") == similarity_request.gender) & (Tag("category") == similarity_request.category)

    # Create queries
    paper_similarity_query = VectorQuery(
        vector=product_img_vector,
        vector_field_name="img_vector",
        num_results=similarity_request.number_of_results,
        return_fields=similarity_request.return_fields,
        filter_expression=filter_expression
    )
    count_query = create_count_query(filter_expression)

    # Execute search
    count, result_papers = await asyncio.gather(
        index.search(count_query),
        index.query(paper_similarity_query)
    )
    # Get Paper records of those results
    return prepare_response(count.total, result_papers)


@r.post("/vectorsearch/text",
       response_model=Dict,
       name="product:find_similar_by_text",
       operation_id="compute_text_similarity")
async def find_products_by_text(similarity_request: SimilarityRequest) -> Dict:
    index = await AsyncSearchIndex.from_existing(
        name=config.INDEX_NAME,
        url=config.REDIS_URL
    )
    # Fetch paper key and the vector from the HASH, cast to numpy array
    product_key = index._get_key({"product_id": similarity_request.product_id}, "product_id")
    product_text_vector = np.frombuffer(
        await index.client.hget(product_key, "text_vector"),
        dtype=np.float32
    )

    # Build filter expression
    filter_expression = (Tag("gender") == similarity_request.gender) & (Tag("category") == similarity_request.category)

    # Create queries
    paper_similarity_query = VectorQuery(
        vector=product_text_vector,
        vector_field_name="text_vector",
        num_results=similarity_request.number_of_results,
        return_fields=similarity_request.return_fields,
        filter_expression=filter_expression
    )
    count_query = create_count_query(filter_expression)

    # Execute search
    count, result_papers = await asyncio.gather(
        index.search(count_query),
        index.query(paper_similarity_query)
    )
    # Get Paper records of those results
    return prepare_response(count.total, result_papers)


# @r.post("/vectorsearch/text/user",
#        response_model=t.Dict,
#        name="product:find_similar_by_user_text",
#        operation_id="compute_user_text_similarity")
# async def find_products_by_user_text(similarity_request: UserTextSimilarityRequest) -> t.Dict:
#     query = create_query(
#         similarity_request.return_fields,
#         similarity_request.search_type,
#         similarity_request.number_of_results,
#         vector_field_name="text_vector",
#         gender=similarity_request.gender,
#         category=similarity_request.category
#     )
#     count_query = count(
#         gender=similarity_request.gender,
#         category=similarity_request.category
#     )

#     # obtain vector from text model in top level  __init__.py
#     vector = TEXT_MODEL.encode(similarity_request.user_text)

#     # obtain results of the query
#     total, results = await asyncio.gather(
#         redis_client.ft(config.INDEX_NAME).search(count_query),
#         redis_client.ft(config.INDEX_NAME).search(query, query_params={"vec_param": vector})
#     )

#     # Get Product records of those results
#     return await products_from_results(total.total, results)
