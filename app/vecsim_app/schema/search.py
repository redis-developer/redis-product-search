import typing as t
from pydantic import BaseModel, Field


class SimilarityRequest(BaseModel):
    product_id: int
    number_of_results: int = 15
    search_type: str = "KNN"
    gender: str = ""
    category: str = ""

class SearchRequest(BaseModel):
    text: str
    number_of_results: int = 15


class UserTextSimilarityRequest(BaseModel):
    user_text: str
    number_of_results: int = 15
    search_type: str = "KNN"
