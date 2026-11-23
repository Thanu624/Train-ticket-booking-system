import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ticketApi } from '../api/ticketApi';
import { paymentApi } from '../api/paymentApi';

const paymentMethods = [
  { id: 'UPI', label: 'UPI', icon: '📲' },
  { id: 'CARD', label: 'Credit / Debit Card', icon: '💳' },
  { id: 'NETBANKING', label: 'Net Banking', icon: '🏦' },
  { id: 'WALLET', label: 'Wallet', icon: '👛' },
];

export default function PaymentPage() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const { train, trainClass, journeyDate, passenger } = state || {};

  const [method, setMethod] = useState('UPI');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!train || !trainClass || !passenger) {
    navigate('/');
    return null;
  }

  const handlePay = async () => {
    setLoading(true);
    setError('');
    try {
      // 1. Book ticket
      const bookRes = await ticketApi.book({
        train_id: train.id,
        train_class_id: trainClass.id,
        passenger_id: passenger.id,
        journey_date: journeyDate,
      });
      const ticket = bookRes.data.data;

      // 2. Process payment
      const payRes = await paymentApi.process({
        ticket_id: ticket.id,
        amount: trainClass.fare,
        payment_method: method,
      });
      const payment = payRes.data.data;

      navigate('/confirmation', { state: { ticket, payment, train, trainClass, passenger } });
    } catch (err) {
      setError(err.response?.data?.message || err.response?.data?.detail || 'Payment failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-full bg-gray-950 p-6">
      <div className="max-w-xl mx-auto">
        <button onClick={() => navigate(-1)} className="text-gray-500 hover:text-gray-300 text-sm mb-4">← Back</button>
        <h1 className="text-2xl font-bold text-white mb-6">Complete Payment</h1>

        {/* Summary */}
        <div className="bg-gray-900 border border-white/10 rounded-xl p-5 mb-6">
          <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Booking Summary</h2>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Train</span>
              <span className="text-white font-medium">{train.train_name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Route</span>
              <span className="text-white">{train.source} → {train.destination}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Journey Date</span>
              <span className="text-white">{journeyDate}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Class</span>
              <span className="text-white">{trainClass.class_type}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Passenger</span>
              <span className="text-white">{passenger.name} ({passenger.age} yrs)</span>
            </div>
            <div className="border-t border-white/10 pt-2 mt-2 flex justify-between">
              <span className="text-white font-semibold">Total Amount</span>
              <span className="text-green-400 font-bold text-lg">₹{trainClass.fare}</span>
            </div>
          </div>
        </div>

        {/* Payment Method */}
        <div className="bg-gray-900 border border-white/10 rounded-xl p-5 mb-6">
          <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-4">Payment Method</h2>
          <div className="grid grid-cols-2 gap-3">
            {paymentMethods.map(pm => (
              <label key={pm.id}
                className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-all ${method === pm.id ? 'border-purple-500 bg-purple-500/10' : 'border-white/10 hover:border-white/20'}`}>
                <input type="radio" name="method" value={pm.id} checked={method === pm.id}
                  onChange={() => setMethod(pm.id)} className="accent-purple-500" />
                <span className="text-lg">{pm.icon}</span>
                <span className="text-sm text-white font-medium">{pm.label}</span>
              </label>
            ))}
          </div>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg p-3 text-sm mb-4">{error}</div>
        )}

        <button onClick={handlePay} disabled={loading}
          className="w-full bg-green-600 hover:bg-green-700 disabled:opacity-60 text-white font-bold py-4 rounded-xl transition-colors shadow-lg shadow-green-500/20 text-lg">
          {loading ? '⏳ Processing...' : `💳 Pay ₹${trainClass.fare}`}
        </button>
        <p className="text-center text-xs text-gray-600 mt-3">🔒 Simulated payment — no real money charged</p>
      </div>
    </div>
  );
}
