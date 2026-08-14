import React, { useState } from 'react';
import api from '../api';
import { useNavigate } from 'react-router-dom';

export default function ProjectCreate({ onProjectCreated }) {
  const [name, setName] = useState('');
  const navigate = useNavigate();
  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await api.post('/projects', { name, country: 'India', building_code: 'NBC-2016' });
    if (res.data) {
      navigate('/projects');
    }
  };
  return (
    <div className="bg-white p-6 rounded shadow max-w-md">
      <h2 className="text-2xl mb-4">New Project</h2>
      <form onSubmit={handleSubmit}>
        <input className="w-full border p-2 mb-4" value={name} onChange={e => setName(e.target.value)} placeholder="Project Name" required />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">Create</button>
      </form>
    </div>
  );
}