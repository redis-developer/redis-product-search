import typing as t
from aredis_om import (
    EmbeddedJsonModel,
    Field,
    HashModel,
    JsonModel
)

# Product Models
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
    image_url: str
    brand: str = Field(index=True)

class Product(JsonModel):
    product_id: int = Field(index=True)
    product_metadata: ProductMetadata

class ProductVectors(HashModel):
    product_id: int
    gender: str
    category: str
    img_vector: bytes
    text_vector: bytes

# User models
class User(JsonModel):
    id: int = Field(index=True)
    email: str = Field(index=True)
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    company: str = Field(index=True)
    title: str = Field(index=True)
    hashed_password: str
