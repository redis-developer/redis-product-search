//  Inspired by https://github.com/marmelab/admin-on-rest/blob/master/docs/Tutorial.md
import { BASE_URL } from '../config';
import { fetchUtils } from 'react-admin';
import simpleRestProvider from 'ra-data-simple-rest';

const httpClient = (url, options) => {
    if (!options) {
      options = {};
    }
    if (!options.headers) {
      options.headers = new Headers({ Accept: 'application/json' });
    }
    const token = localStorage.getItem('token');
    options.headers.set('Authorization', `Bearer ${token}`);
    return fetchUtils.fetchJson(url, options);
  };

  // TODO Implement custom data provider to fix the id problem with users
export const dataProvider = simpleRestProvider(BASE_URL + "/api/v1", httpClient);
