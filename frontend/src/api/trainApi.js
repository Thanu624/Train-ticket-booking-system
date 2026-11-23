import axiosClient from './axiosClient';

export const trainApi = {
  search: (source, destination, date) =>
    axiosClient.get('/trains/search', { params: { source, destination, journey_date: date } }),
  getAll: (page = 1, size = 20) =>
    axiosClient.get('/trains', { params: { page, size } }),
  getById: (id) => axiosClient.get(`/trains/${id}`),
  add: (data) => axiosClient.post('/trains', data),
  update: (id, data) => axiosClient.put(`/trains/${id}`, data),
  delete: (id) => axiosClient.delete(`/trains/${id}`),
};
