import typing as t
from pydantic import BaseModel, Field

DEFAULT_RETURN_FIELDS = ["product_id", "product_pk", "vector_score"]

class SimilarityRequest(BaseModel):
    product_id: int
    number_of_results: int = 15
    search_type: str = "KNN"
    gender: str = ""
    category: str = ""
    return_fields: list = DEFAULT_RETURN_FIELDS

class SearchRequest(BaseModel):
    text: str
    number_of_results: int = 15
    return_fields: list = DEFAULT_RETURN_FIELDS

class UserTextSimilarityRequest(BaseModel):
    user_text: str
    number_of_results: int = 15
    search_type: str = "KNN"
    gender: str = ""
    category: str = ""
    return_fields: list = DEFAULT_RETURN_FIELDS
