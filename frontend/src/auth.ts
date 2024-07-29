import decodeJwt from 'jwt-decode';
import { BASE_URL } from './config';


export const isAuthenticated = () => {
  const permissions = localStorage.getItem('permissions');
  if (!permissions) {
    return false;
  }
  return permissions === 'user' || permissions === 'admin' ? true : false;
};

/**
 * Login to master and store JSON web token on success
 *
 * @param email
 * @param password
 * @returns JSON data containing access token on success
 * @throws Error on http errors or failed attempts
 */
export const login = async (email: string, password: string) => {
  // Assert email or password is not empty
  if (!(email.length > 0) || !(password.length > 0)) {
    throw new Error('Email or password was not provided');
  }
  const formData = new FormData();
  // OAuth2 expects form data, not JSON data
  formData.append('username', email);
  formData.append('password', password);

  const request = new Request(BASE_URL + '/api/token', {
    method: 'POST',
    body: formData
  }
  );

  const response = await fetch(request);

  if (response.status === 500) {
    throw new Error('Internal server error');
  }

  const data = await response.json();

  if (response.status > 400 && response.status < 500) {
    if (data.detail) {
      throw data.detail;
    }
    throw data;
  }

  if ('access_token' in data) {
    const decodedToken: any = decodeJwt(data['access_token']);
    localStorage.setItem('token', data['access_token']);
    localStorage.setItem('permissions', decodedToken.permissions);
  }

  return data;
};

/**
 * Sign up via master and store JSON web token on success
 *
 * @param email
 * @param password
 * @returns JSON data containing access token on success
 * @throws Error on http errors or failed attempts
 */
export const signUp = async (
  first: string,
  last: string,
  email: string,
  password: string,
  passwordConfirmation: string,
  company: string,
  title: string
) => {
  // Assert first and last name are not empty
  if (!(first.length > 0) || !(last.length > 0)) {
    throw new Error('First or last name was not provided');
  }
  if (!(email.length > 0)) {
    throw new Error('Email was not provided');
  }
  if (!(password.length > 0)) {
    throw new Error('Password was not provided');
  }
  if (!(passwordConfirmation.length > 0)) {
    throw new Error('Password confirmation was not provided');
  }
  if (!(company.length > 0)) {
    throw new Error('Company was not provided');
  }
  if (!(title.length > 0)) {
    throw new Error('Title was not provided');
  }


  const formData = new FormData();
  // OAuth2 expects form data, not JSON data
  formData.append('username', email);
  formData.append('password', password);

  const url = BASE_URL + `/api/signup?first=${first}&last=${last}&company=${company}&title=${title}`;
  const request = new Request(url, {
    method: 'POST',
    body: formData
  });

  const response = await fetch(request);

  if (response.status === 500) {
    throw new Error('Internal server error');
  }

  const data = await response.json();
  if (response.status > 400 && response.status < 500) {
    if (data.detail) {
      throw data.detail;
    }
    throw data;
  }

  if ('access_token' in data) {
    const decodedToken: any = decodeJwt(data['access_token']);
    localStorage.setItem('token', data['access_token']);
    localStorage.setItem('permissions', decodedToken.permissions);
  }

  return data;
};

export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('permissions');
};
