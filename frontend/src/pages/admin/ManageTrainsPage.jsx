import React, { useEffect, useState } from 'react';
import { trainApi } from '../../api/trainApi';

const emptyTrain = {
  train_number: '', train_name: '', source: '', destination: '',
  departure_time: '', arrival_time: '',
};

export default function ManageTrainsPage() {
  const [trains, setTrains] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyTrain);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchTrains = () => {
    setLoading(true);
    trainApi.getAll(1, 100)
      .then(r => setTrains(r.data.data?.items || r.data.data || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetchTrains(); }, []);

  const handleEdit = (train) => {
    setEditing(train);
    setForm({
      train_number: train.train_number,
      train_name: train.train_name,
      source: train.source,
      destination: train.destination,
      departure_time: train.departure_time,
      arrival_time: train.arrival_time,
    });
    setShowForm(true);
    setError('');
  };

  const handleNew = () => {
    setEditing(null);
    setForm(emptyTrain);
    setShowForm(true);
    setError('');
  };

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');
    try {
      if (editing) {
        await trainApi.update(editing.id, form);
        setSuccess('Train updated successfully!');
      } else {
        await trainApi.add(form);
        setSuccess('Train added successfully!');
      }
      setShowForm(false);
      fetchTrains();
    } catch (err) {
      setError(err.response?.data?.message || err.response?.data?.detail || 'Operation failed');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this train?')) return;
    try {
      await trainApi.delete(id);
      setSuccess('Train deleted.');
      fetchTrains();
    } catch (err) {
      alert(err.response?.data?.message || 'Delete failed');
    }
  };

  return (
    <div className="min-h-full bg-gray-950 p-6">
      <div className="max-w-5xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-white">🚂 Manage Trains</h1>
            <p className="text-gray-400 text-sm mt-0.5">{trains.length} trains in system</p>
          </div>
          <button onClick={handleNew}
            className="bg-purple-600 hover:bg-purple-700 text-white font-semibold px-4 py-2.5 rounded-lg transition-colors text-sm">
            + Add Train
          </button>
        </div>

        {success && <div className="bg-green-500/10 border border-green-500/30 text-green-400 rounded-lg p-3 text-sm mb-4">{success}</div>}

        {/* Form */}
        {showForm && (
          <div className="bg-gray-900 border border-purple-500/30 rounded-xl p-5 mb-6">
            <h2 className="text-lg font-bold text-white mb-4">{editing ? 'Edit Train' : 'Add New Train'}</h2>
            {error && <div className="bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg p-3 text-sm mb-4">{error}</div>}
            <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
              {[
                { name: 'train_number', label: 'Train Number', placeholder: '12951' },
                { name: 'train_name', label: 'Train Name', placeholder: 'Mumbai Rajdhani' },
                { name: 'source', label: 'Source', placeholder: 'Mumbai' },
                { name: 'destination', label: 'Destination', placeholder: 'Delhi' },
                { name: 'departure_time', label: 'Departure Time', placeholder: '16:35' },
                { name: 'arrival_time', label: 'Arrival Time', placeholder: '08:35' },
              ].map(f => (
                <div key={f.name}>
                  <label className="block text-xs text-gray-400 mb-1">{f.label}</label>
                  <input name={f.name} value={form[f.name]} onChange={handleChange} required
                    placeholder={f.placeholder}
                    className="w-full bg-gray-800 border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500" />
                </div>
              ))}
              <div className="col-span-2 flex gap-3 mt-2">
                <button type="submit" disabled={saving}
                  className="bg-purple-600 hover:bg-purple-700 disabled:opacity-60 text-white font-semibold px-6 py-2.5 rounded-lg text-sm transition-colors">
                  {saving ? 'Saving...' : (editing ? 'Update Train' : 'Add Train')}
                </button>
                <button type="button" onClick={() => setShowForm(false)}
                  className="bg-gray-800 hover:bg-gray-700 text-white px-6 py-2.5 rounded-lg text-sm border border-white/10 transition-colors">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Table */}
        {loading ? (
          <div className="flex justify-center py-16">
            <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="bg-gray-900 border border-white/10 rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/5">
                  {['Number', 'Name', 'Source', 'Destination', 'Departure', 'Arrival', 'Actions'].map(h => (
                    <th key={h} className="text-left text-xs font-semibold text-gray-500 uppercase tracking-wider px-4 py-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {trains.map(t => (
                  <tr key={t.id} className="hover:bg-white/2 transition-colors">
                    <td className="px-4 py-3 font-mono text-purple-300">{t.train_number}</td>
                    <td className="px-4 py-3 text-white font-medium">{t.train_name}</td>
                    <td className="px-4 py-3 text-gray-400">{t.source}</td>
                    <td className="px-4 py-3 text-gray-400">{t.destination}</td>
                    <td className="px-4 py-3 text-gray-300">{t.departure_time}</td>
                    <td className="px-4 py-3 text-gray-300">{t.arrival_time}</td>
                    <td className="px-4 py-3">
                      <div className="flex gap-2">
                        <button onClick={() => handleEdit(t)} className="text-xs text-blue-400 hover:text-blue-300 border border-blue-500/30 hover:border-blue-400/50 px-2.5 py-1 rounded transition-all">Edit</button>
                        <button onClick={() => handleDelete(t.id)} className="text-xs text-red-400 hover:text-red-300 border border-red-500/30 hover:border-red-400/50 px-2.5 py-1 rounded transition-all">Delete</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {trains.length === 0 && <p className="text-center text-gray-500 py-8">No trains found.</p>}
          </div>
        )}
      </div>
    </div>
  );
}
