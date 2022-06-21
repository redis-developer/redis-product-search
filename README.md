
## Redis Vector Search

This demo showcases the vector search similarity (VSS) capability within Redis Stack.


https://user-images.githubusercontent.com/13009163/174868872-81de3f6f-fea6-405d-954c-a8c15c6c41f8.mov


The following Redis capabilities are available in this demo:
 - Vector Similarity Search with RedisSearch
    - Visual embedding search with Pytorch and img2vec
    - Semantic embedding search with Huggingface and RoBerta
 - Full text search
 - Document based storage with RedisJSON

### Datasets

The dataset was taken from the the following Kaggle links.

- [Large Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)
- [Smaller Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small)


## Stack

This demo was built as a Single Page Application (SPA) with the following components

#### Backend
 - FastAPI
 - Redis OM
 - RedisPy
 - Pydantic

#### Database
 - Redis Stack: Redis with RedisJSON and RedisSearch Modules (amoungst others)

#### Front End
 - Typescript + React
 - React-bootstrap

