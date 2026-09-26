'use client';
import React, { useState } from 'react';
import { uploadCsv } from '@/lib/api';

export const CsvUploader = ({ onUploadSuccess }: { onUploadSuccess: () => void }) => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setError(null);
    try {
      await uploadCsv(file);
      onUploadSuccess();
      setFile(null);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow border border-gray-200 max-w-md">
      <h3 className="text-lg font-semibold mb-4">Upload Instagram Analytics CSV</h3>
      <div className="flex flex-col gap-4">
        <input 
          type="file" 
          accept=".csv" 
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
        />
        {error && <p className="text-red-500 text-sm">{error}</p>}
        <button
          onClick={handleUpload}
          disabled={!file || uploading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md font-medium disabled:bg-gray-300 hover:bg-blue-700 transition-colors"
        >
          {uploading ? 'Uploading...' : 'Analyse Data'}
        </button>
      </div>
    </div>
  );
};
