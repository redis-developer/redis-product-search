FROM node:18.8-alpine AS ReactImage

WORKDIR /app/gui

ENV NODE_PATH=/app/gui/node_modules
ENV PATH=$PATH:/app/gui/node_modules/.bin

COPY ./gui/package.json ./
RUN yarn install --no-optional

ADD ./gui ./
RUN yarn build

FROM python:3.9-slim-buster AS ApiImage

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN python3 -m pip install --upgrade pip setuptools wheel

WORKDIR /app/
COPY ./data/ ./data

RUN mkdir -p /app/backend
WORKDIR /app/backend

COPY ./backend/ .
RUN pip install -e . --no-cache-dir

# add static react files to fastapi image
COPY --from=ReactImage /app/gui/build /app/backend/productsearch/templates/build

LABEL org.opencontainers.image.source https://github.com/RedisVentures/redis-product-search

WORKDIR /app/backend/productsearch

CMD ["sh", "./entrypoint.sh"]