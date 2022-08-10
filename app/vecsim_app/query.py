import typing as t
from redis.asyncio import Redis
from redis.commands.search.field import VectorField, TagField
from redis.commands.search.query import Query


async def create_flat_index(
    redis_conn: Redis,
    number_of_vectors: int,
    distance_metric: str='L2'
):
    image_field = VectorField("img_vector",
                "FLAT", {
                    "TYPE": "FLOAT32",
                    "DIM": 512,
                    "DISTANCE_METRIC": distance_metric,
                    "INITIAL_CAP": number_of_vectors,
                    "BLOCK_SIZE":number_of_vectors
                })
    text_field = VectorField("text_vector",
                "FLAT", {
                    "TYPE": "FLOAT32",
                    "DIM": 768,
                    "DISTANCE_METRIC": distance_metric,
                    "INITIAL_CAP": number_of_vectors,
                    "BLOCK_SIZE":number_of_vectors
                })
    category_field = TagField("category")
    gender_field = TagField("gender")
    await redis_conn.ft().create_index([image_field,
                                        text_field,
                                        category_field,
                                        gender_field])


async def create_hnsw_index(
    redis_conn: Redis,
    number_of_vectors: int,
    distance_metric: str='COSINE'
):
    image_field = VectorField("img_vector",
                "HNSW", {
                    "TYPE": "FLOAT32",
                    "DIM": 512,
                    "DISTANCE_METRIC": distance_metric,
                    "INITIAL_CAP": number_of_vectors,
                })
    text_field = VectorField("text_vector",
                "HNSW", {
                    "TYPE": "FLOAT32",
                    "DIM": 768,
                    "DISTANCE_METRIC": distance_metric,
                    "INITIAL_CAP": number_of_vectors,
                })
    category_field = TagField("category")
    gender_field = TagField("gender")
    await redis_conn.ft().create_index([image_field,
                                        text_field,
                                        category_field,
                                        gender_field])


async def create_query(
    search_type: str="KNN",
    number_of_results: int=20,
    vector_field_name: str="img_vector",
    gender: t.Optional[str] = None,
    category: t.Optional[str] = None
):
    tag = "("
    if gender:
        tag += f"@gender:{{{gender}}}"
    if category:
        tag += f"@category:{{{category}}}"
    tag += ")"
    # if no tags are selected
    if len(tag) < 3:
        tag = "*"

    base_query = f'{tag}=>[{search_type} {number_of_results} @{vector_field_name} $vec_param AS vector_score]'
    q = Query(base_query)
    q.sort_by("vector_score")
    q.paging(0, number_of_results)
    q.return_fields("product_id", "product_pk", "vector_score")
    q.dialect(2)
    return q
