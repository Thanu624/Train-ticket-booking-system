import React from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';

const statusColor = {
  BOOKED: 'bg-green-500/20 text-green-300 border-green-500/30',
  WAITING: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30',
  RAC: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
  CANCELLED: 'bg-red-500/20 text-red-300 border-red-500/30',
};

const paymentStatusColor = {
  SUCCESS: 'text-green-400',
  PENDING: 'text-yellow-400',
  FAILED: 'text-red-400',
};

export default function ConfirmationPage() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const { ticket, payment, train, trainClass, passenger } = state || {};

  if (!ticket) return (
    <div className="min-h-full bg-gray-950 flex items-center justify-center">
      <div className="text-center">
        <p className="text-gray-400 mb-4">No booking found.</p>
        <button onClick={() => navigate('/')} className="text-purple-400 hover:text-purple-300">Go Home</button>
      </div>
    </div>
  );

  return (
    <div className="min-h-full bg-gray-950 p-6">
      <div className="max-w-xl mx-auto">
        {/* Success Banner */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-green-500/20 rounded-full border border-green-500/30 mb-4">
            <span className="text-4xl">✅</span>
          </div>
          <h1 className="text-2xl font-bold text-white">Booking Confirmed!</h1>
          <p className="text-gray-400 mt-1">Your ticket has been booked successfully.</p>
        </div>

        {/* PNR Card */}
        <div className="bg-gradient-to-br from-purple-900/40 to-blue-900/30 border border-purple-500/30 rounded-2xl p-6 mb-6 text-center">
          <p className="text-gray-400 text-sm mb-1">PNR Number</p>
          <p className="text-4xl font-black text-white tracking-widest font-mono">{ticket.pnr_number}</p>
          <p className="text-xs text-gray-500 mt-2">Keep this PNR for reference</p>
          <div className={`inline-flex items-center mt-3 px-3 py-1 rounded-full border text-sm font-medium ${statusColor[ticket.ticket_status] || 'bg-gray-700 text-gray-300'}`}>
            {ticket.ticket_status}
          </div>
        </div>

        {/* Details */}
        <div className="bg-gray-900 border border-white/10 rounded-xl p-5 mb-6 space-y-3 text-sm">
          {[
            { label: 'Train', value: `${train?.train_name} (${train?.train_number})` },
            { label: 'Route', value: `${train?.source} → ${train?.destination}` },
            { label: 'Journey Date', value: ticket.journey_date },
            { label: 'Class', value: trainClass?.class_type },
            { label: 'Seat', value: `${ticket.coach_number}-${ticket.seat_number}` },
            { label: 'Passenger', value: `${passenger?.name} (${passenger?.age} yrs, ${passenger?.gender})` },
            { label: 'Fare', value: `₹${payment?.amount}` },
            { label: 'Payment', value: payment?.payment_status, colored: true },
          ].map(({ label, value, colored }) => (
            <div key={label} className="flex justify-between">
              <span className="text-gray-500">{label}</span>
              <span className={`font-medium ${colored ? paymentStatusColor[value] || 'text-white' : 'text-white'}`}>{value}</span>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-2 gap-3">
          <Link to="/my-bookings"
            className="bg-purple-600 hover:bg-purple-700 text-white text-center font-semibold py-3 rounded-xl transition-colors">
            📋 My Bookings
          </Link>
          <Link to="/"
            className="bg-gray-800 hover:bg-gray-700 text-white text-center font-semibold py-3 rounded-xl transition-colors border border-white/10">
            🏠 Home
          </Link>
        </div>
      </div>
    </div>
  );
}
