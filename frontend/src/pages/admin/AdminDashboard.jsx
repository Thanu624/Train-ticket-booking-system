import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { trainApi } from '../../api/trainApi';
import { ticketApi } from '../../api/ticketApi';

export default function AdminDashboard() {
  const [stats, setStats] = useState({ trains: 0, tickets: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      trainApi.getAll(1, 100),
      ticketApi.getAll(1, 100),
    ]).then(([trainRes, ticketRes]) => {
      setStats({
        trains: trainRes.data.data?.total || trainRes.data.data?.length || 0,
        tickets: ticketRes.data.data?.total || ticketRes.data.data?.length || 0,
      });
    }).catch(() => {}).finally(() => setLoading(false));
  }, []);

  const cards = [
    { label: 'Total Trains', value: stats.trains, icon: '🚂', color: 'from-purple-600 to-purple-800', link: '/admin/trains' },
    { label: 'Total Tickets', value: stats.tickets, icon: '🎫', color: 'from-blue-600 to-blue-800', link: null },
    { label: 'Manage Trains', value: 'Add / Edit', icon: '⚙️', color: 'from-orange-600 to-orange-800', link: '/admin/trains' },
    { label: 'Manage Classes', value: 'Add / Edit', icon: '🪑', color: 'from-green-600 to-green-800', link: '/admin/classes' },
  ];

  return (
    <div className="min-h-full bg-gray-950 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">Admin Dashboard</h1>
          <p className="text-gray-400 text-sm mt-1">Manage trains, classes, and monitor bookings</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {cards.map((c, i) => (
            c.link ? (
              <Link key={i} to={c.link} className={`bg-gradient-to-br ${c.color} rounded-xl p-5 text-white hover:opacity-90 transition-opacity`}>
                <div className="text-3xl mb-2">{c.icon}</div>
                <div className="text-2xl font-bold">{loading ? '...' : c.value}</div>
                <div className="text-sm opacity-80 mt-1">{c.label}</div>
              </Link>
            ) : (
              <div key={i} className={`bg-gradient-to-br ${c.color} rounded-xl p-5 text-white`}>
                <div className="text-3xl mb-2">{c.icon}</div>
                <div className="text-2xl font-bold">{loading ? '...' : c.value}</div>
                <div className="text-sm opacity-80 mt-1">{c.label}</div>
              </div>
            )
          ))}
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <Link to="/admin/trains" className="bg-gray-900 border border-white/10 hover:border-purple-500/40 rounded-xl p-6 transition-all group">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-purple-600/20 rounded-xl flex items-center justify-center text-2xl group-hover:bg-purple-600/30 transition-colors">🚂</div>
              <div>
                <h3 className="text-white font-bold">Manage Trains</h3>
                <p className="text-gray-400 text-sm">Add, edit, or remove train entries</p>
              </div>
            </div>
          </Link>
          <Link to="/admin/classes" className="bg-gray-900 border border-white/10 hover:border-green-500/40 rounded-xl p-6 transition-all group">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-green-600/20 rounded-xl flex items-center justify-center text-2xl group-hover:bg-green-600/30 transition-colors">🪑</div>
              <div>
                <h3 className="text-white font-bold">Manage Classes</h3>
                <p className="text-gray-400 text-sm">Configure fare, seats per class</p>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}
