const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export async function uploadCsv(file: File) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/analytics/analyse`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Upload failed');
  }

  return response.json();
}

export async function getAnalyticsSummary() {
  const response = await fetch(`${API_BASE_URL}/analytics/summary`);
  if (!response.ok) throw new Error('Failed to fetch summary');
  return response.json();
}

export async function getTopPosts() {
  const response = await fetch(`${API_BASE_URL}/analytics/top-posts`);
  if (!response.ok) throw new Error('Failed to fetch top posts');
  return response.json();
}

export async function getFormatPerformance() {
  const response = await fetch(`${API_BASE_URL}/analytics/by-format`);
  if (!response.ok) throw new Error('Failed to fetch format performance');
  return response.json();
}

export async function getTimeline() {
  const response = await fetch(`${API_BASE_URL}/analytics/timeline`);
  if (!response.ok) throw new Error('Failed to fetch timeline');
  return response.json();
}
