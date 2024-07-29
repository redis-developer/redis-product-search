from pydantic import BaseModel

from productsearch.config import DEFAULT_RETURN_FIELDS


class BaseRequest(BaseModel):
    number_of_results: int = 15
    search_type: str = "KNN"
    gender: str = ""
    category: str = ""
    return_fields: list = DEFAULT_RETURN_FIELDS

class SimilarityRequest(BaseRequest):
    product_id: int


# class SearchRequest(BaseModel):
#     text: str
#     number_of_results: int = 15
#     return_fields: list = DEFAULT_RETURN_FIELDS

class UserTextSimilarityRequest(BaseRequest):
    user_text: str
