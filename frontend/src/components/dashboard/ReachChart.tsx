'use client';
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface TimelineData {
  date: string;
  reach: number;
  engagements: number;
  post_count: number;
}

export const ReachChart = ({ data }: { data: TimelineData[] }) => (
  <div className="bg-white p-4 rounded-lg shadow border border-gray-200 h-80">
    <h3 className="text-md font-semibold mb-4 text-gray-700">Reach & Engagement Over Time</h3>
    <ResponsiveContainer width="100%" height="90%">
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="date" tick={{fontSize: 12}} />
        <YAxis tick={{fontSize: 12}} />
        <Tooltip />
        <Line type="monotone" dataKey="reach" stroke="#2563eb" strokeWidth={2} dot={{r: 4}} name="Reach" />
        <Line type="monotone" dataKey="engagements" stroke="#10b981" strokeWidth={2} dot={{r: 4}} name="Engagements" />
      </LineChart>
    </ResponsiveContainer>
  </div>
);
