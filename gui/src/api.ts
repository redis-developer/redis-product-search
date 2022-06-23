import { MASTER_URL } from './config';

// get products from Redis through the FastAPI backend
export const getProducts = async (limit=20, skip=0) => {
  const response = await fetch(MASTER_URL + '?limit=' + limit + '&skip=' + skip);
  const data = await response.json();
  if (data) { return data; }

  return Promise.reject('Failed to get message from backend');
};

export const getProductsByText = async (search_text: string, limit=20, skip=0) => {
  // TODO use limit and skip to paginate through search results
  let body = {
    text: search_text,
    number_of_results: limit
  }

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
};

  const response = await fetch(MASTER_URL + 'search?limit=' + limit, requestOptions);
  const data = await response.json();
  if (data) { return data; }

  return Promise.reject('Failed to search for products from backend');
};


export const getVisuallySimilarProducts = async (id: number, search='KNN', limit=20, skip=0) => {

  let body = {
    product_id: id,
    search_type: search,
    number_of_results: limit
  }

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
};

  const response = await fetch(MASTER_URL + "vectorsearch/image", requestOptions);
  const data = await response.json();
  if (data) { return data; }

  return Promise.reject('Failed to get similar products from backend');
};


export const getSemanticallySimilarProducts = async (id: number, search='KNN', limit=20, skip=0) => {

  let body = {
    product_id: id,
    search_type: search,
    number_of_results: limit
  }

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
};

  const response = await fetch(MASTER_URL + "vectorsearch/text", requestOptions);
  const data = await response.json();
  if (data) { return data; }

  return Promise.reject('Failed to get similar products from backend');
};
