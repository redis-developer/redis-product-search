from pydantic import BaseModel


class Product(BaseModel):
    product_id: str
    name: str
    gender: str
    category: str
    img_url: str
    text_vector: str
    img_vector: str


class VectorSearchProduct(Product):
    vector_distance: float
    similarity_score: float

    def __init__(self, *args, **kwargs):
        kwargs["similarity_score"] = 1 - float(kwargs["vector_distance"])
        super().__init__(*args, **kwargs)


class BaseRequest(BaseModel):
    number_of_results: int = 15
    search_type: str = "KNN"
    gender: str = ""
    category: str = ""


class SimilarityRequest(BaseRequest):
    product_id: int


class SearchRequest(BaseModel):
    text: str
    number_of_results: int = 15


class UserTextSimilarityRequest(BaseRequest):
    user_text: str


class ProductSearchResponse(BaseModel):
    total: int
    products: list[Product]


class ProductVectorSearchResponse(BaseModel):
    total: int
    products: list[VectorSearchProduct]
