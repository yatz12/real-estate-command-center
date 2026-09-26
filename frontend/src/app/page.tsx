import React from 'react';

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {['Reach', 'Impressions', 'Views', 'Engagement Rate'].map((metric) => (
          <div key={metric} className="p-4 bg-white rounded-lg shadow border border-gray-200">
            <div className="text-sm text-gray-500">{metric}</div>
            <div className="text-2xl font-bold text-gray-800">--</div>
          </div>
        ))}
      </div>
      <div className="p-8 bg-white rounded-lg shadow border border-gray-200 text-center text-gray-400">
        Chart Placeholder: Upload a CSV to see data
      </div>
    </div>
  );
}
