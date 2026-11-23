import axiosClient from './axiosClient';

export const paymentApi = {
  process: (data) => axiosClient.post('/payments/process', data),
  getByTicket: (ticketId) => axiosClient.get(`/payments/ticket/${ticketId}`),
  getAll: (page = 1, size = 20) => axiosClient.get('/payments', { params: { page, size } }),
};
