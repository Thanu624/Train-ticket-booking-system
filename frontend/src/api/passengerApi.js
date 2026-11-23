import axiosClient from './axiosClient';

export const passengerApi = {
  getAll: () => axiosClient.get('/passengers'),
  add: (data) => axiosClient.post('/passengers', data),
  update: (id, data) => axiosClient.put(`/passengers/${id}`, data),
  delete: (id) => axiosClient.delete(`/passengers/${id}`),
};
