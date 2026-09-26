'use client';
import React, { useEffect, useState } from 'react';
import { getAnalyticsSummary, getTopPosts, getFormatPerformance, getTimeline } from '@/lib/api';
import { MetricCard } from '@/components/dashboard/MetricCard';
import { ReachChart } from '@/components/dashboard/ReachChart';
import { ContentPerformance } from '@/components/dashboard/ContentPerformance';
import { TopPosts } from '@/components/dashboard/TopPosts';
import { CsvUploader } from '@/components/upload/CsvUploader';

export default function Dashboard() {
  const [summary, setSummary] = useState<any>(null);
  const [topPosts, setTopPosts] = useState<any[]>([]);
  const [formatData, setFormatData] = useState<any[]>([]);
  const [timeline, setTimeline] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [s, tp, fp, tl] = await Promise.all([
        getAnalyticsSummary(),
        getTopPosts(),
        getFormatPerformance(),
        getTimeline(),
      ]);
      setSummary(s);
      setTopPosts(tp);
      setFormatData(fp);
      setTimeline(tl);
    } catch (e) {
      console.error("Error fetching analytics:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <div className="flex items-center justify-center h-full text-gray-500">Loading...</div>;

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Content Intelligence Dashboard</h2>
        <CsvUploader onUploadSuccess={fetchData} />
      </div>

      {!summary || summary.total_posts === 0 ? (
        <div className="p-20 bg-white rounded-lg shadow border border-gray-200 text-center">
          <p className="text-gray-500 mb-4">No data available. Please upload an Instagram analytics CSV to start.</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <MetricCard title="Total Posts" value={summary.total_posts} />
            <MetricCard title="Total Reach" value={summary.total_reach.toLocaleString()} />
            <MetricCard title="Total Views" value={summary.total_views.toLocaleString()} />
            <MetricCard title="Avg Engagement Rate" value={`${summary.average_engagement_rate}%`} />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ReachChart data={timeline} />
            <ContentPerformance data={formatData} />
          </div>

          <TopPosts posts={topPosts} />
        </>
      )}
    </div>
  );
}
