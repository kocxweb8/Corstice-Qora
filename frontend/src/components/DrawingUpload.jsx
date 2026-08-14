import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import api from '../api';

export default function DrawingUpload() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [uploading, setUploading] = useState(false);
  const [drawingId, setDrawingId] = useState(null);
  const { getRootProps, getInputProps } = useDropzone({
    accept: { 'application/dxf': ['.dxf'] },
    onDrop: async (files) => {
      setUploading(true);
      const formData = new FormData();
      formData.append('file', files[0]);
      const res = await api.post(`/drawings/${id}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setDrawingId(res.data.id);
      await api.post(`/drawings/${res.data.id}/parse`);
      setUploading(false);
      navigate(`/project/${id}/viewer`);
    }
  });
  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-2xl mb-4">Upload DXF Drawing</h2>
      <div {...getRootProps()} className="border-2 border-dashed p-12 text-center cursor-pointer">
        <input {...getInputProps()} />
        {uploading ? 'Uploading...' : 'Drag & drop DXF file here, or click to select'}
      </div>
      {drawingId && <p className="mt-2 text-green-600">Uploaded successfully!</p>}
    </div>
  );
}