import typing as t
from pydantic import FileUrl, BaseModel
from aredis_om import JsonModel, EmbeddedJsonModel, Field



class ProductMetadata(EmbeddedJsonModel):
    name: str = Field(index=True, full_text_search=True)
    gender: str = Field(index=True)
    master_category: str = Field(index=True)
    sub_category: str = Field(index=True)
    article_type: str = Field(index=True)
    base_color: str = Field(index=True)
    season: str = Field(index=True)
    year: int = Field(index=True)
    usage: str = Field(index=True)

class Product(JsonModel):
    product_id: int = Field(index=True)
    product_metadata: ProductMetadata

class SimilarityRequest(BaseModel):
    product_id: int
    number_of_results: int = 10
    search_type: str = "KNN"

class SearchRequest(BaseModel):
    text: str
    number_of_results: int = 10