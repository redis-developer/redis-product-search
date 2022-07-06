
<div align="center">
    <a href="https://github.com/spartee/redis-vector-search"><img src="https://github.com/Spartee/redis-vector-search/blob/master/app/vecsim_app/data/redis-logo.png?raw=true" width="30%"><img></a>
    <br />
    <br />
<div display="inline-block">
    <a href="https://github.com/Spartee/redis-vector-search"><b>Code</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://redis.io/docs/stack/search/reference/vectors/"><b>Redis VSS Documentation</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://discord.gg/hd5RRGpykv"><b>Discord Invite</b></a>&nbsp;&nbsp;&nbsp;
  </div>
    <br />
    <br />
</div>

# Redis Vector Search Demo Application

This demo showcases the vector search similarity (VSS) capability within Redis Stack and Redis Enterprise.
Through the RediSearch module, vector types and indexes can be added to Redis. This turns Redis into
a highly performant vector database which can be used for all types of applications.

The following Redis Stack capabilities are available in this demo:
   - **Vector Similarity Search** 
     - by image
     - by text
   - **Multiple vector indexing types**
     - HNSW
     - Flat (brute-force)
   - **Hybrid Queries**
     - Apply tags as pre-filter for vector search
   - **Full text search** 
   - **JSON storage** 


## Application

This app was built as a Single Page Application (SPA) with the following components:

- **[Redis Stack](https://redis.io/docs/stack/)**: Vector database + JSON storage
- **[FastAPI](https://fastapi.tiangolo.com/)** (Python 3.8)
  - JWT authentication using [OAuth2 "password
    flow"](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/) and
    PyJWT
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** for schema and validation
- **[React](https://reactjs.org/)** (with Typescript)
- **[Redis OM](https://redis.io/docs/stack/get-started/tutorials/stack-python/)** for ORM
- **[Docker Compose](https://docs.docker.com/compose/)** for development
- **[MaterialUI](https://material-ui.com/)** for some UI elements
- **[React-Bootstrap](https://react-bootstrap.github.io/)** for some UI elements
- **[react-admin](https://github.com/marmelab/react-admin)** for the admin dashboard
  - Using the same token based authentication as FastAPI backend (JWT)
- **[Pytorch/Img2Vec](https://github.com/christiansafka/img2vec)** and **[Huggingface Sentence Transformers](https://huggingface.co/sentence-transformers)** for vector embedding creation

Some inspiration was taken from this [Cookiecutter project](https://github.com/Buuntu/fastapi-react)
and turned into a SPA application instead of a separate front-end server approach.


### Datasets

The dataset was taken from the the following Kaggle links.

- [Large Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)
- [Smaller Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small)


## Running Locally

MORE TO COME HERE

There are multiple options for running this demo locally.

### Using pre-built containers

The easiest option to run locally is to use the following docker-compose file to launch the
prebuilt container hosted on GitHub.

```
version: '3.7'
services:

  redis-vector-db:
    image: redis/redis-stack:latest
    ports:
      - 6379:6379
      - 8001:8001

  backend:
    image: ghcr.io/spartee/redis-vss-fashion:v0.1.3
    environment:
      DEPLOYMENT: "dev"
      REDIS_DATA_URL: 'redis://redis-vector-db:6379'
      REDIS_OM_URL: 'redis://redis-vector-db:6379'
      REDIS_HOST: 'redis-vector-db'
      REDIS_PORT: 6379
    expose:
      - "8888"
    ports:
      - "8888:8888"
    depends_on:
      - "redis-vector-db"
```

To launch, run the following
- ``docker compose up`` in same directory as ``docker-compose.yml``
- Navigate to ``0.0.0.0:8888`` in a browser

### Building the containers

More to come here

### Running outside docker

More to come here
