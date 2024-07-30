FROM node:22.0-alpine AS ReactImage

WORKDIR /app/frontend

ENV NODE_PATH=/app/frontend/node_modules
ENV PATH=$PATH:/app/frontend/node_modules/.bin

COPY ./frontend/package.json ./
RUN npm install

ADD ./frontend ./
RUN npm run build

FROM python:3.11 AS ApiImage

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
COPY --from=ReactImage /app/frontend/build /app/backend/productsearch/templates/build

LABEL org.opencontainers.image.source https://github.com/RedisVentures/redis-product-search

WORKDIR /app/backend/productsearch

CMD ["sh", "./entrypoint.sh"]