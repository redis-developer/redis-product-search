from aredis_om import (
    EmbeddedJsonModel,
    Field,
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
