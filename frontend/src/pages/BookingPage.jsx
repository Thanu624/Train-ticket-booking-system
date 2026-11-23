import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { passengerApi } from '../api/passengerApi';
import { useAuth } from '../context/AuthContext';

export default function BookingPage() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();

  const { train, trainClass, journeyDate } = state || {};

  const [passengers, setPassengers] = useState([]);
  const [selectedPassenger, setSelectedPassenger] = useState(null);
  const [addNew, setAddNew] = useState(false);
  const [newP, setNewP] = useState({ name: '', age: '', gender: 'MALE', mobile_number: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!train) navigate('/');
    passengerApi.getAll().then(r => setPassengers(r.data.data || [])).catch(() => {});
  }, []);

  const handleAddPassenger = async (e) => {
    e.preventDefault();
    setError('');
    if (!/^\d{10}$/.test(newP.mobile_number)) {
      setError('Mobile number must be 10 digits');
      return;
    }
    setLoading(true);
    try {
      const res = await passengerApi.add({ ...newP, age: parseInt(newP.age) });
      const p = res.data.data;
      setPassengers([...passengers, p]);
      setSelectedPassenger(p);
      setAddNew(false);
      setNewP({ name: '', age: '', gender: 'MALE', mobile_number: '' });
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to add passenger');
    } finally {
      setLoading(false);
    }
  };

  const handleProceed = () => {
    if (!selectedPassenger) {
      setError('Please select or add a passenger');
      return;
    }
    navigate('/payment', { state: { train, trainClass, journeyDate, passenger: selectedPassenger } });
  };

  if (!train || !trainClass) return null;

  return (
    <div className="min-h-full bg-gray-950 p-6">
      <div className="max-w-2xl mx-auto">
        <button onClick={() => navigate(-1)} className="text-gray-500 hover:text-gray-300 text-sm mb-4">← Back</button>
        <h1 className="text-2xl font-bold text-white mb-6">Book Ticket</h1>

        {/* Train Summary */}
        <div className="bg-gray-900 border border-white/10 rounded-xl p-5 mb-6">
          <div className="flex items-center justify-between mb-3">
            <div>
              <span className="text-xs bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded font-mono mr-2">{train.train_number}</span>
              <span className="text-white font-bold">{train.train_name}</span>
            </div>
            <span className="text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded">{trainClass.class_type}</span>
          </div>
          <div className="flex items-center gap-4 text-sm text-gray-400">
            <span>📍 {train.source} → {train.destination}</span>
            <span>📅 {journeyDate}</span>
            <span className="text-green-400 font-semibold">₹{trainClass.fare}</span>
          </div>
        </div>

        {/* Passenger Selection */}
        <div className="bg-gray-900 border border-white/10 rounded-xl p-5 mb-6">
          <h2 className="text-lg font-bold text-white mb-4">Select Passenger</h2>

          {passengers.length > 0 && (
            <div className="space-y-2 mb-4">
              {passengers.map(p => (
                <label key={p.id} className={`flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-all ${selectedPassenger?.id === p.id ? 'border-purple-500 bg-purple-500/10' : 'border-white/10 hover:border-white/20'}`}>
                  <input
                    type="radio"
                    name="passenger"
                    checked={selectedPassenger?.id === p.id}
                    onChange={() => { setSelectedPassenger(p); setAddNew(false); }}
                    className="accent-purple-500"
                  />
                  <div>
                    <p className="text-white font-medium">{p.name}</p>
                    <p className="text-xs text-gray-400">{p.age} yrs · {p.gender} · 📱 {p.mobile_number}</p>
                  </div>
                </label>
              ))}
            </div>
          )}

          <button
            onClick={() => { setAddNew(!addNew); setSelectedPassenger(null); }}
            className="text-purple-400 hover:text-purple-300 text-sm font-medium transition-colors"
          >
            {addNew ? '✕ Cancel' : '+ Add New Passenger'}
          </button>

          {addNew && (
            <form onSubmit={handleAddPassenger} className="mt-4 space-y-3 border-t border-white/5 pt-4">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-gray-400 mb-1">Full Name</label>
                  <input value={newP.name} onChange={e => setNewP({...newP, name: e.target.value})} required
                    className="w-full bg-gray-800 border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500"
                    placeholder="Passenger Name" />
                </div>
                <div>
                  <label className="block text-xs text-gray-400 mb-1">Age</label>
                  <input type="number" value={newP.age} onChange={e => setNewP({...newP, age: e.target.value})} required min="1" max="120"
                    className="w-full bg-gray-800 border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500"
                    placeholder="Age" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-gray-400 mb-1">Gender</label>
                  <select value={newP.gender} onChange={e => setNewP({...newP, gender: e.target.value})}
                    className="w-full bg-gray-800 border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500">
                    <option value="MALE">Male</option>
                    <option value="FEMALE">Female</option>
                    <option value="OTHER">Other</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-gray-400 mb-1">Mobile</label>
                  <input value={newP.mobile_number} onChange={e => setNewP({...newP, mobile_number: e.target.value})} required maxLength={10}
                    className="w-full bg-gray-800 border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500"
                    placeholder="10-digit number" />
                </div>
              </div>
              {error && <p className="text-red-400 text-xs">{error}</p>}
              <button type="submit" disabled={loading}
                className="bg-purple-600 hover:bg-purple-700 disabled:opacity-60 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors">
                {loading ? 'Adding...' : 'Save Passenger'}
              </button>
            </form>
          )}
        </div>

        {error && !addNew && <p className="text-red-400 text-sm mb-4">{error}</p>}

        <button onClick={handleProceed}
          className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3.5 rounded-xl transition-colors shadow-lg shadow-purple-500/25">
          Proceed to Payment →
        </button>
      </div>
    </div>
  );
}
