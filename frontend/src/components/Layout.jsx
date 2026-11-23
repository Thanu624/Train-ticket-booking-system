import React, { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const navLinks = [
  { to: '/', label: 'Home', icon: '🏠', end: true },
  { to: '/search', label: 'Search Trains', icon: '🔍' },
  { to: '/pnr-status', label: 'PNR Status', icon: '📋' },
];

const myAccountLinks = [
  { to: '/my-bookings', label: 'My Tickets', icon: '🎫' },
];

const adminLinks = [
  { to: '/admin', label: 'Dashboard', icon: '📊', end: true },
  { to: '/admin/trains', label: 'Manage Trains', icon: '🚂' },
  { to: '/admin/classes', label: 'Manage Classes', icon: '🪑' },
];

export default function Layout() {
  const { user, logout, isAdmin } = useAuth();
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const SidebarContent = () => (
    <div className="flex flex-col h-full">
      {/* Logo */}
      <div className="flex items-center gap-3 px-6 py-5 border-b border-white/10">
        <div className="w-9 h-9 bg-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-lg">🚂</div>
        <div>
          <span className="text-white font-bold text-lg">RailBook</span>
          <span className="text-purple-400 font-bold text-lg"> Pro</span>
        </div>
      </div>

      {/* Nav */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-6">
        <div>
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider px-3 mb-2">Navigation</p>
          {navLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.end}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all mb-1 ${
                  isActive
                    ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/25'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`
              }
              onClick={() => setSidebarOpen(false)}
            >
              <span>{link.icon}</span>
              {link.label}
            </NavLink>
          ))}
        </div>

        <div>
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider px-3 mb-2">My Account</p>
          {myAccountLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all mb-1 ${
                  isActive
                    ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/25'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`
              }
              onClick={() => setSidebarOpen(false)}
            >
              <span>{link.icon}</span>
              {link.label}
            </NavLink>
          ))}
        </div>

        {isAdmin() && (
          <div>
            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wider px-3 mb-2">Admin</p>
            {adminLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.end}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all mb-1 ${
                    isActive
                      ? 'bg-orange-600 text-white'
                      : 'text-gray-400 hover:text-white hover:bg-white/5'
                  }`
                }
                onClick={() => setSidebarOpen(false)}
              >
                <span>{link.icon}</span>
                {link.label}
              </NavLink>
            ))}
          </div>
        )}
      </div>

      {/* Logout */}
      <div className="px-3 py-4 border-t border-white/10">
        <button
          onClick={handleLogout}
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-red-400 hover:text-white hover:bg-red-500/20 w-full transition-all"
        >
          <span>🚪</span> Logout
        </button>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen bg-gray-950 overflow-hidden">
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex flex-col w-56 bg-gray-900 border-r border-white/10 flex-shrink-0">
        <SidebarContent />
      </aside>

      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-50 flex md:hidden">
          <div className="fixed inset-0 bg-black/60" onClick={() => setSidebarOpen(false)} />
          <aside className="relative z-50 flex flex-col w-56 bg-gray-900">
            <SidebarContent />
          </aside>
        </div>
      )}

      {/* Main Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="flex items-center justify-between px-4 py-3 bg-gray-900 border-b border-white/10 flex-shrink-0">
          <button className="md:hidden text-gray-400 hover:text-white" onClick={() => setSidebarOpen(true)}>
            ☰
          </button>
          <div className="hidden md:block" />
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 text-sm text-gray-300">
              <span className="w-7 h-7 bg-purple-600 rounded-full flex items-center justify-center text-white font-bold text-xs">
                {user?.first_name?.[0]?.toUpperCase() || 'U'}
              </span>
              <span>{user?.first_name} {user?.last_name}</span>
              {isAdmin() && <span className="bg-orange-500 text-white text-xs px-2 py-0.5 rounded-full">ADMIN</span>}
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-1.5 bg-red-600 hover:bg-red-700 text-white text-sm px-3 py-1.5 rounded-lg transition-colors"
            >
              🚪 Logout
            </button>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
