
<div align="center">
    <a href="https://github.com/spartee/redis-vector-search"><img src="https://redis.io/wp-content/uploads/2024/04/Logotype.svg?raw=true" width="30%"><img></a>
    <br />
    <br />
<div display="inline-block">
    <a href="https://ecommerce.redisvl.com/"><b>Hosted Demo</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/redis-developer/redis-product-search"><b>Code</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://redis.io/docs/stack/search/reference/vectors/"><b>Redis VSS Documentation</b></a>&nbsp;&nbsp;&nbsp;
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

## Application

This app was built as a Single Page Application (SPA) with the following components:

- **[Redis Stack](https://redis.io/docs/stack/)**: Vector database + JSON storage
- **[RedisVL](https://redisvl.com)** for Python vector db client
- **[FastAPI](https://fastapi.tiangolo.com/)** for backend API
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** for schema and validation
- **[React](https://reactjs.org/)** (with Typescript)
- **[Docker Compose](https://docs.docker.com/compose/)** for development
- **[MaterialUI](https://material-ui.com/)** for some UI elements
- **[React-Bootstrap](https://react-bootstrap.github.io/)** for some UI elements
- **[Pytorch/Img2Vec](https://github.com/christiansafka/img2vec)** and **[Huggingface Sentence Transformers](https://huggingface.co/sentence-transformers)** for vector embedding creation

Some inspiration was taken from this [Cookiecutter project](https://github.com/Buuntu/fastapi-react)
and turned into a SPA application instead of a separate front-end server approach.

### General Project Structure

Much inspiration taken from [tiangelo/full-stack-fastapi-template](https://github.com/tiangolo/full-stack-fastapi-template)

```
/backend
    /productsearch
        /api
            /routes
                product.py # primary API logic lives here
        /db
            load.py # seeds Redis DB
            redis_helpers.py # redis util
        /schema
            # pydantic models for serialization/validation from API
        /tests
        /utils
        config.py
        spa.py # logic for serving compiled react project
        main.py # entrypoint
/frontend
    /public
        # index, manifest, logos, etc.
    /src
        /config
        /styles
        /views
            # primary components live here

        api.ts # logic for connecting with BE
        App.tsx # project entry
        Routes.tsk # route definitions
        ...
/data
    # folder mounted as volume in Docker
    # load script auto populates initial data from S3

```

### Datasets

The dataset was taken from the the following Kaggle links.

- [Large Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset)
- [Smaller Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-small)

A formatted version is available for use with this demo at:


## Running the App with docker-compose
Before running the app, install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

1. Copy .env file

```bash
cp template.env .env
```

2. Run docker containers with `make`

```bash
make build
```

Note: you can add `--build` and `--force-recreate` if caching old images.

## Running local without docker-compose

### Run frontend

1. Install NPM packages
    ```bash
    $ cd frontend/
    $ npm install
    ````
2. Use `npm` to serve the application from your machine
    ```bash
    $ npm run start
    ```
3. Navigate to `http://localhost:3000` in a browser.

All changes to your local code will be reflected in your display in semi realtime.

### Run backend
Pre-step: install [poetry](https://python-poetry.org/).

1. `cd backend`
2. `poetry install` to get necessary python deps
3. `poetry run start` to launch uvicorn server with FastAPI app

### vscode debugger

Included in the project is a `./vscode/launch.json` for local debugging purposes.

### Troubleshooting
Sometimes you need to clear out some Docker cached artifacts. Run `docker system prune`, restart Docker Desktop, and try again.

Open an issue here on GitHub and we will try to be responsive to these. Additionally, please consider [contributing](CONTRIBUTING.md).