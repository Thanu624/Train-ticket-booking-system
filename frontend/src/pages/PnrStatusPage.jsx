import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ticketApi } from '../api/ticketApi';

const statusColor = {
  BOOKED: 'bg-green-500/20 text-green-300 border-green-500/30',
  WAITING: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
  RAC: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
  CANCELLED: 'bg-red-500/20 text-red-300 border-red-500/30',
};

export default function PnrStatusPage() {
  const navigate = useNavigate();
  const [pnr, setPnr] = useState('');
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!pnr.trim()) return;
    setLoading(true);
    setError('');
    setTicket(null);
    try {
      const res = await ticketApi.getByPnr(pnr.trim().toUpperCase());
      setTicket(res.data.data);
    } catch (err) {
      setError(err.response?.data?.message || 'PNR not found');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 p-6">
      <div className="max-w-xl mx-auto">
        {/* Header */}
        <div className="flex items-center gap-3 mb-8">
          <button onClick={() => navigate('/login')} className="text-gray-500 hover:text-gray-300 text-sm">← Login</button>
          <div className="flex items-center gap-2">
            <span className="text-2xl">🚂</span>
            <span className="text-xl font-bold text-white">RailBook<span className="text-purple-400"> Pro</span></span>
          </div>
        </div>

        <h1 className="text-2xl font-bold text-white mb-2">PNR Status</h1>
        <p className="text-gray-400 text-sm mb-6">Enter your PNR to check ticket status (no login required)</p>

        <form onSubmit={handleSearch} className="flex gap-3 mb-6">
          <input
            value={pnr}
            onChange={e => setPnr(e.target.value)}
            className="flex-1 bg-gray-900 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 uppercase font-mono tracking-wider"
            placeholder="e.g. PNR1234567"
          />
          <button type="submit" disabled={loading}
            className="bg-purple-600 hover:bg-purple-700 disabled:opacity-60 text-white font-semibold px-6 py-3 rounded-lg transition-colors">
            {loading ? '...' : '🔍 Search'}
          </button>
        </form>

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg p-4 text-sm">{error}</div>
        )}

        {ticket && (
          <div className="bg-gray-900 border border-white/10 rounded-xl overflow-hidden">
            {/* PNR Header */}
            <div className="bg-gradient-to-r from-purple-900/40 to-blue-900/30 p-5 text-center border-b border-white/5">
              <p className="text-gray-400 text-xs mb-1">PNR Number</p>
              <p className="text-3xl font-black text-white font-mono tracking-widest">{ticket.pnr_number}</p>
              <span className={`inline-flex mt-2 px-3 py-1 rounded-full border text-sm font-medium ${statusColor[ticket.ticket_status] || 'bg-gray-700'}`}>
                {ticket.ticket_status}
              </span>
            </div>

            {/* Details */}
            <div className="p-5 space-y-3 text-sm">
              {[
                { label: 'Journey Date', value: ticket.journey_date },
                { label: 'Seat', value: `${ticket.coach_number} - Seat ${ticket.seat_number}` },
                { label: 'Ticket ID', value: `#${ticket.id}` },
              ].map(({ label, value }) => (
                <div key={label} className="flex justify-between">
                  <span className="text-gray-500">{label}</span>
                  <span className="text-white font-medium">{value}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
