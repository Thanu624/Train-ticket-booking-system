import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { trainApi } from '../api/trainApi';
import { trainClassApi } from '../api/trainClassApi';

const classBadgeColor = {
  SL: 'bg-blue-500/20 text-blue-300',
  '3A': 'bg-green-500/20 text-green-300',
  '2A': 'bg-yellow-500/20 text-yellow-300',
  '1A': 'bg-orange-500/20 text-orange-300',
  CC: 'bg-purple-500/20 text-purple-300',
  EC: 'bg-pink-500/20 text-pink-300',
  '2S': 'bg-teal-500/20 text-teal-300',
  GN: 'bg-gray-500/20 text-gray-300',
};

function TrainCard({ train, journeyDate, navigate }) {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    trainClassApi.getForTrain(train.id)
      .then(r => setClasses(r.data.data || []))
      .catch(() => setClasses([]))
      .finally(() => setLoading(false));
  }, [train.id]);

  const availableClasses = classes.filter(c => c.available_seats > 0);

  return (
    <div className="bg-gray-900 border border-white/10 rounded-xl overflow-hidden hover:border-purple-500/30 transition-all">
      <div className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded font-mono">{train.train_number}</span>
            </div>
            <h3 className="text-lg font-bold text-white">{train.train_name}</h3>
          </div>
          <div className="text-right">
            {availableClasses.length > 0 ? (
              <span className="text-xs bg-green-500/20 text-green-300 px-2 py-1 rounded-full">
                ✓ Available
              </span>
            ) : (
              <span className="text-xs bg-red-500/20 text-red-300 px-2 py-1 rounded-full">
                ✗ Full
              </span>
            )}
          </div>
        </div>

        {/* Route & Time */}
        <div className="flex items-center gap-3 mb-4">
          <div className="text-center">
            <p className="text-xl font-bold text-white">{train.departure_time}</p>
            <p className="text-sm text-gray-400">{train.source}</p>
          </div>
          <div className="flex-1 flex items-center gap-2">
            <div className="flex-1 h-px bg-gradient-to-r from-purple-500 to-blue-500" />
            <span className="text-xs text-gray-500">🚂</span>
            <div className="flex-1 h-px bg-gradient-to-r from-blue-500 to-purple-500" />
          </div>
          <div className="text-center">
            <p className="text-xl font-bold text-white">{train.arrival_time}</p>
            <p className="text-sm text-gray-400">{train.destination}</p>
          </div>
        </div>

        {/* Classes */}
        {!loading && (
          <div className="flex flex-wrap gap-2 mb-4">
            {classes.map(c => (
              <span key={c.id} className={`text-xs px-2 py-1 rounded font-medium ${classBadgeColor[c.class_type] || 'bg-gray-700 text-gray-300'}`}>
                {c.class_type} · ₹{c.fare} · {c.available_seats} seats
              </span>
            ))}
          </div>
        )}

        {/* Book buttons */}
        {expanded && (
          <div className="border-t border-white/5 pt-4 mt-2">
            <p className="text-sm text-gray-400 mb-3 font-medium">Select Class to Book:</p>
            <div className="grid grid-cols-2 gap-2">
              {classes.map(c => (
                <button
                  key={c.id}
                  disabled={c.available_seats === 0}
                  onClick={() => navigate('/booking', { state: { train, trainClass: c, journeyDate } })}
                  className={`flex items-center justify-between px-3 py-2.5 rounded-lg border text-sm font-medium transition-all ${
                    c.available_seats > 0
                      ? 'border-purple-500/40 bg-purple-500/10 text-purple-300 hover:bg-purple-500/20'
                      : 'border-gray-700 bg-gray-800 text-gray-600 cursor-not-allowed'
                  }`}
                >
                  <span>{c.class_type}</span>
                  <span>₹{c.fare}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        <button
          onClick={() => setExpanded(!expanded)}
          className="w-full text-center text-sm text-purple-400 hover:text-purple-300 mt-3 py-1 transition-colors"
        >
          {expanded ? '▲ Hide Classes' : '▼ View Classes & Book'}
        </button>
      </div>
    </div>
  );
}

export default function SearchResultsPage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const source = params.get('source') || '';
  const destination = params.get('destination') || '';
  const date = params.get('date') || '';

  const [trains, setTrains] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!source || !destination || !date) return;
    setLoading(true);
    trainApi.search(source, destination, date)
      .then(r => setTrains(r.data.data || []))
      .catch(err => setError(err.response?.data?.message || 'Search failed'))
      .finally(() => setLoading(false));
  }, [source, destination, date]);

  return (
    <div className="min-h-full bg-gray-950 p-6">
      <div className="max-w-3xl mx-auto">
        <div className="flex items-center gap-2 mb-2">
          <button onClick={() => navigate('/')} className="text-gray-500 hover:text-gray-300 text-sm">← Back</button>
        </div>
        <h1 className="text-2xl font-bold text-white mb-1">
          {source} → {destination}
        </h1>
        <p className="text-gray-400 text-sm mb-6">📅 {date}</p>

        {loading && (
          <div className="flex justify-center py-16">
            <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
          </div>
        )}

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg p-4 text-sm">{error}</div>
        )}

        {!loading && !error && trains.length === 0 && (
          <div className="text-center py-16">
            <span className="text-5xl mb-4 block">🚫</span>
            <p className="text-gray-400 text-lg">No trains found for this route.</p>
            <button onClick={() => navigate('/')} className="mt-4 text-purple-400 hover:text-purple-300 text-sm">Search another route</button>
          </div>
        )}

        <div className="space-y-4">
          {trains.map(train => (
            <TrainCard key={train.id} train={train} journeyDate={date} navigate={navigate} />
          ))}
        </div>
      </div>
    </div>
  );
}
