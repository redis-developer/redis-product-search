FROM node:22.0-alpine AS ReactImage

WORKDIR /app/frontend

ENV NODE_PATH=/app/frontend/node_modules
ENV PATH=$PATH:/app/frontend/node_modules/.bin

COPY ./frontend/package.json ./
RUN npm install

ADD ./frontend ./
RUN npm run build

FROM python:3.11-slim-buster AS ApiImage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app/
VOLUME [ "/data" ]

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN mkdir -p /app/backend

# copy deps first so we don't have to reload everytime
COPY ./backend/poetry.lock ./backend/pyproject.toml ./backend/

WORKDIR /app/backend
RUN poetry install --all-extras --no-interaction

COPY ./backend/ .

# add static react files to fastapi image
COPY --from=ReactImage /app/frontend/build /app/backend/productsearch/templates/build

LABEL org.opencontainers.image.source https://github.com/RedisVentures/redis-product-search

CMD ["poetry", "run", "start-app"]