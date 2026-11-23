import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { trainApi } from '../api/trainApi';

const popularRoutes = [
  { from: 'Mumbai', to: 'Delhi' },
  { from: 'Bangalore', to: 'Chennai' },
  { from: 'Hyderabad', to: 'Mumbai' },
  { from: 'Kolkata', to: 'Delhi' },
  { from: 'Chennai', to: 'Pune' },
  { from: 'Delhi', to: 'Jaipur' },
];

export default function HomePage() {
  const navigate = useNavigate();
  const today = new Date().toISOString().split('T')[0];
  const [form, setForm] = useState({ source: '', destination: '', journey_date: today });
  const [error, setError] = useState('');

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSearch = (e) => {
    e.preventDefault();
    if (!form.source || !form.destination || !form.journey_date) {
      setError('Please fill in all fields.');
      return;
    }
    setError('');
    navigate(`/search?source=${encodeURIComponent(form.source)}&destination=${encodeURIComponent(form.destination)}&date=${form.journey_date}`);
  };

  const handlePopular = (route) => {
    setForm({ ...form, source: route.from, destination: route.to });
  };

  return (
    <div className="min-h-full bg-gray-950">
      {/* Hero */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/30 via-gray-950 to-blue-900/20 pointer-events-none" />
        <div className="relative max-w-4xl mx-auto px-4 pt-16 pb-10 text-center">
          <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 rounded-full px-4 py-1.5 text-sm text-purple-300 mb-6">
            ✨ India's Smartest Train Booking Platform
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold text-white leading-tight mb-3">
            Book Train Tickets
          </h1>
          <h1 className="text-4xl md:text-5xl font-extrabold text-purple-400 leading-tight mb-4">
            Fast &amp; Effortlessly
          </h1>
          <p className="text-gray-400 text-lg mb-10">
            Search trains, compare classes, and book tickets with real-time seat availability.
          </p>

          {/* Search Box */}
          <div className="bg-gray-900/80 backdrop-blur border border-white/10 rounded-2xl p-6 shadow-2xl">
            <form onSubmit={handleSearch}>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-left">
                  <label className="block text-xs font-semibold text-gray-400 mb-1.5">📍 From</label>
                  <input
                    name="source"
                    value={form.source}
                    onChange={handleChange}
                    className="w-full bg-gray-800 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                    placeholder="e.g. Mumbai"
                  />
                </div>
                <div className="text-left">
                  <label className="block text-xs font-semibold text-gray-400 mb-1.5">📍 To</label>
                  <input
                    name="destination"
                    value={form.destination}
                    onChange={handleChange}
                    className="w-full bg-gray-800 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                    placeholder="e.g. Delhi"
                  />
                </div>
                <div className="text-left">
                  <label className="block text-xs font-semibold text-gray-400 mb-1.5">📅 Journey Date</label>
                  <input
                    type="date"
                    name="journey_date"
                    value={form.journey_date}
                    onChange={handleChange}
                    min={today}
                    className="w-full bg-gray-800 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-purple-500 transition-colors"
                  />
                </div>
              </div>
              {error && <p className="text-red-400 text-sm mt-3">{error}</p>}
              <button
                type="submit"
                className="mt-4 w-full md:w-auto md:px-12 bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors text-base shadow-lg shadow-purple-500/25"
              >
                🔍 Search Trains
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Popular Routes */}
      <div className="max-w-4xl mx-auto px-4 pb-10">
        <p className="text-gray-400 font-semibold mb-3">🔥 Popular Routes</p>
        <div className="flex flex-wrap gap-2">
          {popularRoutes.map((r, i) => (
            <button
              key={i}
              onClick={() => handlePopular(r)}
              className="bg-gray-800 hover:bg-gray-700 border border-white/10 text-gray-300 hover:text-white text-sm px-4 py-2 rounded-full transition-all"
            >
              {r.from} → {r.to}
            </button>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="max-w-4xl mx-auto px-4 pb-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: 'Trains Available', value: '500+', icon: '🚂' },
            { label: 'Routes Covered', value: '200+', icon: '🗺️' },
            { label: 'Happy Passengers', value: '10M+', icon: '😊' },
            { label: 'Bookings Today', value: '50K+', icon: '🎫' },
          ].map((s, i) => (
            <div key={i} className="bg-gray-900 border border-white/10 rounded-xl p-4 text-center">
              <div className="text-2xl mb-1">{s.icon}</div>
              <div className="text-xl font-bold text-white">{s.value}</div>
              <div className="text-xs text-gray-500 mt-0.5">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
