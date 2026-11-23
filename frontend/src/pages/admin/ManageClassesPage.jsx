import React, { useEffect, useState } from 'react';
import { trainApi } from '../../api/trainApi';
import { trainClassApi } from '../../api/trainClassApi';

const classTypes = ['GN', '2S', 'SL', '3A', '2A', '1A', 'CC', 'EC'];

export default function ManageClassesPage() {
  const [trains, setTrains] = useState([]);
  const [selectedTrain, setSelectedTrain] = useState('');
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ class_type: 'SL', fare: '', total_seats: '', train_id: '' });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    trainApi.getAll(1, 100).then(r => setTrains(r.data.data?.items || r.data.data || [])).catch(() => {});
  }, []);

  const fetchClasses = (trainId) => {
    setLoading(true);
    trainClassApi.getForTrain(trainId)
      .then(r => setClasses(r.data.data || []))
      .catch(() => setClasses([]))
      .finally(() => setLoading(false));
  };

  const handleTrainSelect = (e) => {
    setSelectedTrain(e.target.value);
    setClasses([]);
    if (e.target.value) fetchClasses(e.target.value);
    setForm(f => ({ ...f, train_id: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');
    try {
      await trainClassApi.add({
        ...form,
        fare: parseFloat(form.fare),
        total_seats: parseInt(form.total_seats),
        train_id: parseInt(selectedTrain),
      });
      setSuccess('Class added!');
      setShowForm(false);
      fetchClasses(selectedTrain);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to add class');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this class?')) return;
    try {
      await trainClassApi.delete(id);
      setSuccess('Class deleted.');
      fetchClasses(selectedTrain);
    } catch (err) {
      alert(err.response?.data?.message || 'Delete failed');
    }
  };

  return (
    <div className="min-h-full bg-gray-950 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-2xl font-bold text-white">🪑 Manage Classes</h1>
            <p className="text-gray-400 text-sm mt-0.5">Configure class types, fare, and seat capacity</p>
          </div>
        </div>

        {success && <div className="bg-green-500/10 border border-green-500/30 text-green-400 rounded-lg p-3 text-sm mb-4">{success}</div>}

        {/* Train selector */}
        <div className="bg-gray-900 border border-white/10 rounded-xl p-5 mb-6">
          <label className="block text-sm font-medium text-gray-400 mb-2">Select Train</label>
          <select value={selectedTrain} onChange={handleTrainSelect}
            className="w-full bg-gray-800 border border-white/10 rounded-lg px-4 py-2.5 text-white focus:outline-none focus:border-purple-500">
            <option value="">-- Select a train --</option>
            {trains.map(t => (
              <option key={t.id} value={t.id}>{t.train_number} - {t.train_name}</option>
            ))}
          </select>
        </div>

        {/* Add Class Form */}
        {selectedTrain && (
          <div className="mb-4 flex justify-end">
            <button onClick={() => setShowForm(!showForm)}
              className="bg-green-600 hover:bg-green-700 text-white font-semibold px-4 py-2.5 rounded-lg text-sm transition-colors">
              + Add Class
            </button>
          </div>
        )}

        {showForm && selectedTrain && (
          <div className="bg-gray-900 border border-green-500/30 rounded-xl p-5 mb-6">
            <h2 className="text-lg font-bold text-white mb-4">Add Class</h2>
            {error && <div className="bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg p-3 text-sm mb-4">{error}</div>}
            <form onSubmit={handleSubmit} className="grid grid-cols-3 gap-4">
              <div>
                <label className="block text-xs text-gray-400 mb-1">Class Type</label>
                <select name="class_type" value={form.class_type} onChange={e => setForm({...form, class_type: e.target.value})}
                  className="w-full bg-gray-800 border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500">
                  {classTypes.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-400 mb-1">Fare (₹)</label>
                <input type="number" value={form.fare} onChange={e => setForm({...form, fare: e.target.value})} required min="1"
                  placeholder="1500"
                  className="w-full bg-gray-800 border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500" />
              </div>
              <div>
                <label className="block text-xs text-gray-400 mb-1">Total Seats</label>
                <input type="number" value={form.total_seats} onChange={e => setForm({...form, total_seats: e.target.value})} required min="1"
                  placeholder="72"
                  className="w-full bg-gray-800 border border-white/10 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-purple-500" />
              </div>
              <div className="col-span-3 flex gap-3">
                <button type="submit" disabled={saving}
                  className="bg-green-600 hover:bg-green-700 disabled:opacity-60 text-white font-semibold px-5 py-2 rounded-lg text-sm transition-colors">
                  {saving ? 'Adding...' : 'Add Class'}
                </button>
                <button type="button" onClick={() => setShowForm(false)}
                  className="bg-gray-800 hover:bg-gray-700 text-white px-5 py-2 rounded-lg text-sm border border-white/10">
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Classes Table */}
        {selectedTrain && (
          loading ? (
            <div className="flex justify-center py-8">
              <div className="w-6 h-6 border-2 border-purple-500 border-t-transparent rounded-full animate-spin" />
            </div>
          ) : (
            <div className="bg-gray-900 border border-white/10 rounded-xl overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/5">
                    {['Class', 'Fare', 'Total Seats', 'Available', 'Actions'].map(h => (
                      <th key={h} className="text-left text-xs font-semibold text-gray-500 uppercase tracking-wider px-4 py-3">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {classes.map(c => (
                    <tr key={c.id} className="hover:bg-white/2">
                      <td className="px-4 py-3 text-purple-300 font-semibold">{c.class_type}</td>
                      <td className="px-4 py-3 text-green-400 font-medium">₹{c.fare}</td>
                      <td className="px-4 py-3 text-white">{c.total_seats}</td>
                      <td className="px-4 py-3">
                        <span className={`text-xs px-2 py-0.5 rounded-full ${c.available_seats > 0 ? 'bg-green-500/20 text-green-300' : 'bg-red-500/20 text-red-300'}`}>
                          {c.available_seats}
                        </span>
                      </td>
                      <td className="px-4 py-3">
                        <button onClick={() => handleDelete(c.id)} className="text-xs text-red-400 hover:text-red-300 border border-red-500/30 px-2.5 py-1 rounded transition-all">Delete</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {classes.length === 0 && <p className="text-center text-gray-500 py-8">No classes found for this train.</p>}
            </div>
          )
        )}
      </div>
    </div>
  );
}
