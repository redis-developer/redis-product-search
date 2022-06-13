from redis import Redis
from redis.commands.search.field import VectorField
from redis.commands.search.query import Query


def create_flat_index(redis_conn: Redis,
                      number_of_vectors: int,
                      vector_dimensions: int=512,
                      distance_metric: str='L2'):
        vector_field = VectorField("img_vector",
                    "FLAT", {
                        "TYPE": "FLOAT32",
                        "DIM": vector_dimensions,
                        "DISTANCE_METRIC": distance_metric,
                        "INITIAL_CAP": number_of_vectors,
                        "BLOCK_SIZE":number_of_vectors
                    })
        flat_index = redis_conn.ft().create_index([vector_field])


#def create_hnsw_index (redis_conn,vector_field_name,number_of_vectors, vector_dimensions=512, distance_metric='L2',M=40,EF=200):
#redis_conn.ft().create_index([
#    VectorField(vector_field_name, "HNSW", {"TYPE": "FLOAT32", "DIM": vector_dimensions, "DISTANCE_METRIC": distance_metric, "INITIAL_CAP": number_of_vectors, "M": M, "EF_CONSTRUCTION": EF}),
#    TagField("product_type"),
#    TextField("item_name"),
#    TagField("country")
#])


def create_query(search_type: str="KNN",
                 number_of_results: int=5):
    base_query = f'*=>[{search_type} {number_of_results} @img_vector $vec_param AS vector_score]'
    q = Query(base_query)
    q.sort_by("vector_score")
    q.paging(0, number_of_results)
    q.return_fields("product_id", "product_pk", "vector_score")
    q.dialect(2)
    return q

