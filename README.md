
## Redis Vector Search

This demo showcases the vector search similarity (VSS) capability within Redis Stack.


https://user-images.githubusercontent.com/13009163/174869063-09210162-25be-4d79-bc43-9be8439121d5.mov



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

This app was built as a Single Page Application (SPA) with the following components

### Backend
 - [FastAPI](https://fastapi.tiangolo.com/)
 - [Redis OM](https://redis.io/docs/stack/get-started/tutorials/stack-python/)
 - [Pydantic](https://pydantic-docs.helpmanual.io/)

### Database
 - [Redis Stack](https://redis.io/docs/stack/): Redis with RedisJSON and RedisSearch Modules (amoungst others)

### Front End
 Built from create react app
 - Typescript + React
 - React-bootstrap

 
### ML tooling
 - [Pytorch/Img2Vec](https://github.com/christiansafka/img2vec)
 - [Huggingface Sentence Transformers](https://huggingface.co/sentence-transformers)
 - PyData stack



