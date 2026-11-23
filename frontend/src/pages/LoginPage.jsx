import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { authApi } from '../api/authApi';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await authApi.login(form);
      // Backend returns: { data: { access_token, token_type, user } }
      const { access_token, user } = res.data.data;
      login(access_token, user);
      navigate('/', { replace: true });
    } catch (err) {
      const msg = err.response?.data?.message || err.response?.data?.detail;
      setError(msg || `Login failed — no response from server. Make sure the backend is running on port 8000.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-2">
            <span className="text-3xl">🚂</span>
            <span className="text-3xl font-bold text-white">RailBook<span className="text-purple-400"> Pro</span></span>
          </div>
          <p className="text-gray-400">India's Smartest Train Booking Platform</p>
        </div>

        <div className="bg-gray-900 border border-white/10 rounded-2xl p-8 shadow-2xl">
          <h2 className="text-2xl font-bold text-white mb-6">Welcome Back</h2>

          {error && (
            <div className="bg-red-500/10 border border-red-500/30 text-red-400 rounded-lg px-4 py-3 mb-4 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1.5">Email</label>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={handleChange}
                required
                className="w-full bg-gray-800 border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                placeholder="admin@railbook.com"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-1.5">Password</label>
              <input
                type="password"
                name="password"
                value={form.password}
                onChange={handleChange}
                required
                className="w-full bg-gray-800 border border-white/10 rounded-lg px-4 py-2.5 text-white placeholder-gray-500 focus:outline-none focus:border-purple-500 transition-colors"
                placeholder="••••••••"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-purple-600 hover:bg-purple-700 disabled:opacity-60 text-white font-semibold py-3 rounded-lg transition-colors mt-2"
            >
              {loading ? 'Signing In...' : 'Sign In'}
            </button>
          </form>

          <p className="text-center text-gray-500 text-sm mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-purple-400 hover:text-purple-300 font-medium">Create Account</Link>
          </p>

          {/* Demo credentials — click to auto-fill */}
          <div className="mt-6 p-4 bg-gray-800/50 rounded-lg border border-white/5">
            <p className="text-xs text-gray-500 font-medium mb-2">👇 Click to auto-fill demo credentials:</p>
            <button
              type="button"
              onClick={() => setForm({ email: 'admin@railbook.com', password: 'Test@1234' })}
              className="w-full text-left text-xs text-orange-400 hover:text-orange-300 hover:bg-white/5 px-2 py-1.5 rounded transition-colors mb-1"
            >
              🔴 Admin: admin@railbook.com / Test@1234
            </button>
            <button
              type="button"
              onClick={() => setForm({ email: 'reshma@gmail.com', password: 'Test@1234' })}
              className="w-full text-left text-xs text-purple-400 hover:text-purple-300 hover:bg-white/5 px-2 py-1.5 rounded transition-colors mb-1"
            >
              🟣 User: reshma@gmail.com / Test@1234
            </button>
            <p className="text-xs text-gray-600 mt-1">All accounts password: Test@1234</p>
          </div>
        </div>
      </div>
    </div>
  );
}
