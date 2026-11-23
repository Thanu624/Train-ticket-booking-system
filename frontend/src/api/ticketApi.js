import axiosClient from './axiosClient';

export const ticketApi = {
  book: (data) => axiosClient.post('/tickets/book', data),
  getMyBookings: () => axiosClient.get('/tickets/my-bookings'),
  getByPnr: (pnr) => axiosClient.get(`/tickets/pnr/${pnr}`),
  cancel: (id) => axiosClient.post(`/tickets/${id}/cancel`),
  getAll: (page = 1, size = 20) => axiosClient.get('/tickets', { params: { page, size } }),
};
