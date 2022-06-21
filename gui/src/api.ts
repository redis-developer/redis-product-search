import { MASTER_URL } from './config';


// // Generic helper fucntions for sending API calls to backend
// interface HttpResponse<T> extends Response {
//   parsedBody?: T;
// }
// export async function http<T>(
//   request: RequestInfo
// ): Promise<HttpResponse<T>> {
//   const response: HttpResponse<T> = await fetch(
//     request
//   );
//   response.parsedBody = await response.json();
//   return response;
// }

// export async function get<T>(
//   path: string,
//   args: RequestInit = { method: "get" }
// ): Promise<HttpResponse<T>> {
//   return await http<T>(new Request(path, args));
// };

// export async function post<T>(
//   path: string,
//   body: any,
//   args: RequestInit = { method: "post", body: JSON.stringify(body) }
// ): Promise<HttpResponse<T>>  {
//   return await http<T>(new Request(path, args));
// };

// export async function put<T>(
//   path: string,
//   body: any,
//   args: RequestInit = { method: "put", body: JSON.stringify(body) }
// ): Promise<HttpResponse<T>> {
//   return await http<T>(new Request(path, args));
// };


// get products from Redis through the FastAPI backend
export const getProducts = async (limit=10, skip=0) => {
  const response = await fetch(MASTER_URL + '?limit=' + limit + '&skip=' + skip);
  const data = await response.json();
  if (data) { return data; }

  return Promise.reject('Failed to get message from backend');
};

export const getProductsByText = async (search_text: string, limit=10, skip=0) => {
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

  const response = await fetch(MASTER_URL + "search", requestOptions);
  const data = await response.json();
  if (data) { return data; }

  return Promise.reject('Failed to search for products from backend');
};


export const getVisuallySimilarProducts = async (id: number, search='KNN', limit=10, skip=0) => {

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


export const getSemanticallySimilarProducts = async (id: number, search='KNN', limit=10, skip=0) => {

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


// interface ProductMetadata {
//   name: string;
//   gender: string;
//   master_category: string;
//   sub_category: String;
//   article_type: string;
//   base_color: string;
//   season: string;
//   year: int;
//   usage: string;
// }

// interface Product {
//   product_id: number;
//   product_metadata: ProductMetadata;
//   image_url: string;
// }

// export const getSimilarProducts = async (id, search_type, limit=10, skip=0) => {
//   const response = await put<{Product}>(
//       MASTER_URL + '/' + id,
//       {
//         product_id: id,
//         search_type: search_type,
//         number_of_results: limit,
//       }
//   );
//   return response.parsedBody;
// }