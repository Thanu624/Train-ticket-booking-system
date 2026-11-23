import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import AdminRoute from './AdminRoute';

import LoginPage from '../pages/LoginPage';
import RegisterPage from '../pages/RegisterPage';
import HomePage from '../pages/HomePage';
import SearchResultsPage from '../pages/SearchResultsPage';
import BookingPage from '../pages/BookingPage';
import PaymentPage from '../pages/PaymentPage';
import ConfirmationPage from '../pages/ConfirmationPage';
import MyBookingsPage from '../pages/MyBookingsPage';
import PnrStatusPage from '../pages/PnrStatusPage';
import AdminDashboard from '../pages/admin/AdminDashboard';
import ManageTrainsPage from '../pages/admin/ManageTrainsPage';
import ManageClassesPage from '../pages/admin/ManageClassesPage';
import Layout from '../components/Layout';

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/pnr-status" element={<PnrStatusPage />} />

      {/* Protected (user) */}
      <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
        <Route index element={<HomePage />} />
        <Route path="search" element={<SearchResultsPage />} />
        <Route path="booking" element={<BookingPage />} />
        <Route path="payment" element={<PaymentPage />} />
        <Route path="confirmation" element={<ConfirmationPage />} />
        <Route path="my-bookings" element={<MyBookingsPage />} />

        {/* Admin */}
        <Route path="admin" element={<AdminRoute><AdminDashboard /></AdminRoute>} />
        <Route path="admin/trains" element={<AdminRoute><ManageTrainsPage /></AdminRoute>} />
        <Route path="admin/classes" element={<AdminRoute><ManageClassesPage /></AdminRoute>} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
