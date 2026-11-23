import axiosClient from './axiosClient';

export const trainClassApi = {
  getForTrain: (trainId) => axiosClient.get(`/train-classes/train/${trainId}`),
  add: (data) => axiosClient.post('/train-classes', data),
  update: (id, data) => axiosClient.put(`/train-classes/${id}`, data),
  delete: (id) => axiosClient.delete(`/train-classes/${id}`),
};
