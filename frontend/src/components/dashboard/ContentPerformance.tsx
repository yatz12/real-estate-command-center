'use client';
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface FormatData {
  format: string;
  count: number;
  avg_reach: number;
  avg_engagement: number;
}

export const ContentPerformance = ({ data }: { data: FormatData[] }) => (
  <div className="bg-white p-4 rounded-lg shadow border border-gray-200 h-80">
    <h3 className="text-md font-semibold mb-4 text-gray-700">Performance by Content Type</h3>
    <ResponsiveContainer width="100%" height="90%">
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis dataKey="format" />
        <YAxis />
        <Tooltip />
        <Bar dataKey="avg_reach" fill="#3b82f6" name="Avg Reach" />
        <Bar dataKey="avg_engagement" fill="#10b981" name="Avg Engagement" />
      </BarChart>
    </ResponsiveContainer>
  </div>
);
