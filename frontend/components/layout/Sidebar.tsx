import React from 'react';

export const Sidebar = () => (
  <aside className="w-64 h-screen border-r bg-gray-50 p-4 flex flex-col gap-4">
    <nav className="flex flex-col gap-2">
      <a href="/" className="p-2 rounded bg-blue-100 text-blue-700 font-medium">Dashboard</a>
      <a href="/upload" className="p-2 rounded hover:bg-gray-200 text-gray-600">Upload CSV</a>
    </nav>
  </aside>
);
