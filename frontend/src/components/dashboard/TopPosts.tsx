'use client';
import React from 'react';

interface Post {
  post_id: string;
  caption: string;
  reach: number;
  engagement_rate: number;
  post_type: string;
}

export const TopPosts = ({ posts }: { posts: Post[] }) => (
  <div className="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
    <div className="p-4 border-b bg-gray-50">
      <h3 className="font-semibold text-gray-700">Top Performing Posts (by Reach)</h3>
    </div>
    <table className="w-full text-left text-sm">
      <thead className="bg-gray-50 text-gray-500">
        <tr>
          <th className="p-4 font-medium">Post</th>
          <th className="p-4 font-medium">Type</th>
          <th className="p-4 font-medium text-right">Reach</th>
          <th className="p-4 font-medium text-right">ER%</th>
        </tr>
      </thead>
      <tbody>
        {posts.map((post) => (
          <tr key={post.post_id} className="border-t hover:bg-gray-50">
            <td className="p-4 max-w-xs truncate">{post.caption}</td>
            <td className="p-4">
              <span className="px-2 py-1 text-xs rounded bg-gray-100 text-gray-600">
                {post.post_type}
              </span>
            </td>
            <td className="p-4 text-right font-medium">{post.reach.toLocaleString()}</td>
            <td className="p-4 text-right text-blue-600 font-medium">{post.engagement_rate}%</td>
          </tr>
        ))}
        {posts.length === 0 && (
          <tr>
            <td colSpan={4} className="p-8 text-center text-gray-400">No data available</td>
          </tr>
        )}
      </tbody>
    </table>
  </div>
);
