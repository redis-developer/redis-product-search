import { MASTER_URL, BASE_URL } from './config';
import { logout } from './auth';

export const fetchFromBackend = async (url: string, method: string, body?: any) => {
  const request = new Request(url, {
    method,
    body: JSON.stringify(body),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem("token")}`,
    },
  });

  const response = await fetch(request);

  if (response.status === 500) {
    throw new Error('Internal server error');
  }
  if (response.status === 401 || response.status === 403) {
    logout();
    // redirect to home page
    window.location.href = "/";
  }

  const data = await response.json();

  if (response.status > 400 && response.status < 500) {
    if (data.detail) {
      throw data.detail;
    }
    throw data;
  }

  return data;
}
export const getProducts = async (limit=15, skip=0) => {
  return fetchFromBackend(`${MASTER_URL}?limit=${limit}&skip=${skip}`, 'GET');
}
// get products from Redis through the FastAPI backend

export const getProductsByText = async (search_text: string, limit=15, skip=0) => {
  // TODO use limit and skip to paginate through search results
  let body = {
    text: search_text,
    number_of_results: limit
  }

  const url = MASTER_URL + 'search?limit=' + limit;
  return fetchFromBackend(url, 'POST', body);
};


export const getVisuallySimilarProducts = async (id: number,
                                                search='KNN',
                                                gender="",
                                                category="",
                                                limit=15,
                                                skip=0) => {
  let body = {
    product_id: id,
    search_type: search,
    gender: gender,
    category: category,
    number_of_results: limit
  }

  const url = MASTER_URL + "vectorsearch/image";
  return fetchFromBackend(url, 'POST', body);
};


export const getSemanticallySimilarProducts = async (id: number,
                                                    search='KNN',
                                                    gender="",
                                                    category="",
                                                    limit=15,
                                                    skip=0) => {
  let body = {
    product_id: id,
    search_type: search,
    gender: gender,
    category: category,
    number_of_results: limit
  }

  const url = MASTER_URL + "vectorsearch/text";
  return fetchFromBackend(url, 'POST', body);
};
