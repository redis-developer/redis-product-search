from pydantic import BaseModel

from productsearch.config import DEFAULT_RETURN_FIELDS

# <Card
#                     key={product.pk}
#                     image_path={product.image_url}
#                     name={product.name}
#                     productId={product.product_id}
#                     numProducts={15}
#                     similarity_score={product.similarity_score}
#                     gender={props.gender}
#                     category={props.category}
#                     setProducts={props.setProducts}
#                     setTotal={props.setTotal}
#                   />


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


# class BaseSearchPaper(Paper):
#     # vector embeddings
#     huggingface: str
#     openai: str
#     cohere: str


class BaseRequest(BaseModel):
    number_of_results: int = 15
    search_type: str = "KNN"
    gender: str = ""
    category: str = ""
    return_fields: list = DEFAULT_RETURN_FIELDS


class SimilarityRequest(BaseRequest):
    product_id: int


class SearchRequest(BaseModel):
    text: str
    number_of_results: int = 15
    return_fields: list = DEFAULT_RETURN_FIELDS


class UserTextSimilarityRequest(BaseRequest):
    user_text: str


class ProductSearchResponse(BaseModel):
    total: int
    products: list[Product]


class ProductVectorSearchResponse(BaseModel):
    total: int
    products: list[VectorSearchProduct]
