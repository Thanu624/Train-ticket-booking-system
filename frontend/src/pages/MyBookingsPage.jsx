import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ticketApi } from '../api/ticketApi';

const statusColor = {
  BOOKED: 'bg-green-500/20 text-green-300',
  WAITING: 'bg-yellow-500/20 text-yellow-300',
  RAC: 'bg-blue-500/20 text-blue-300',
  CANCELLED: 'bg-red-500/20 text-red-400 line-through',
};

export default function MyBookingsPage() {
  const navigate = useNavigate();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cancelling, setCancelling] = useState(null);
  const [error, setError] = useState('');

  const fetchBookings = () => {
    setLoading(true);
    ticketApi.getMyBookings()
      .then(r => setTickets(r.data.data || []))
      .catch(() => setError('Failed to load bookings'))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchBookings(); }, []);

  const handleCancel = async (id) => {
    if (!confirm('Cancel this ticket?')) return;
    setCancelling(id);
    try {
      await ticketApi.cancel(id);
      fetchBookings();
    } catch (err) {
      alert(err.response?.data?.message || 'Cancellation failed');
    } finally {
      setCancelling(null);
    }
  };

  return (
    <div className="min-h-full bg-gray-950 p-6">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold text-white mb-6">🎫 My Bookings</h1>

        {loading && (
          <div className="flex justify-center py-16">
            <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {error && <div className="bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg p-4">{error}</div>}

        {!loading && tickets.length === 0 && (
          <div className="text-center py-16">
            <span className="text-5xl mb-4 block">🎫</span>
            <p className="text-gray-400 text-lg mb-4">No bookings yet.</p>
            <button onClick={() => navigate('/')} className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2.5 rounded-lg">
              Book a Ticket
            </button>
          </div>
        )}

        <div className="space-y-4">
          {tickets.map(t => (
            <div key={t.id} className="bg-gray-900 border border-white/10 rounded-xl p-5 hover:border-white/20 transition-all">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <span className="text-xs font-mono bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded mr-2">PNR: {t.pnr_number}</span>
                  <span className={`text-xs px-2 py-0.5 rounded ${statusColor[t.ticket_status] || 'bg-gray-700 text-gray-300'}`}>
                    {t.ticket_status}
                  </span>
                </div>
                {(t.ticket_status === 'BOOKED' || t.ticket_status === 'WAITING' || t.ticket_status === 'RAC') && (
                  <button
                    onClick={() => handleCancel(t.id)}
                    disabled={cancelling === t.id}
                    className="text-xs text-red-400 hover:text-red-300 border border-red-500/30 hover:border-red-400/50 px-3 py-1 rounded-lg transition-all disabled:opacity-50"
                  >
                    {cancelling === t.id ? '...' : '✕ Cancel'}
                  </button>
                )}
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                <div>
                  <p className="text-gray-500 text-xs">Journey Date</p>
                  <p className="text-white font-medium">{t.journey_date}</p>
                </div>
                <div>
                  <p className="text-gray-500 text-xs">Seat</p>
                  <p className="text-white font-medium">{t.coach_number}-{t.seat_number}</p>
                </div>
                <div>
                  <p className="text-gray-500 text-xs">Class</p>
                  <p className="text-white font-medium">{t.train_class_id}</p>
                </div>
                <div>
                  <p className="text-gray-500 text-xs">Ticket ID</p>
                  <p className="text-white font-medium text-xs">#{t.id}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
