import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
}

export const MetricCard = ({ title, value, subtitle }: MetricCardProps) => (
  <div className="p-4 bg-white rounded-lg shadow border border-gray-200">
    <div className="text-sm text-gray-500 font-medium">{title}</div>
    <div className="text-2xl font-bold text-gray-800">{value}</div>
    {subtitle && <div className="text-xs text-gray-400 mt-1">{subtitle}</div>}
  </div>
);
