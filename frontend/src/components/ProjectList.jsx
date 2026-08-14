import React from 'react';
import { Link } from 'react-router-dom';

export default function ProjectList({ projects }) {
  return (
    <div>
      <h2 className="text-2xl mb-4">Your Projects</h2>
      <div className="grid gap-4">
        {projects.map(p => (
          <div key={p.id} className="bg-white p-4 rounded shadow flex justify-between items-center">
            <div>
              <div className="font-bold">{p.name}</div>
              <div className="text-sm text-gray-600">{p.country} - {p.building_code}</div>
              <div className="text-sm">Status: {p.status}</div>
            </div>
            <Link to={`/project/${p.id}`} className="bg-blue-500 text-white px-4 py-2 rounded">Upload Drawing</Link>
          </div>
        ))}
      </div>
      <Link to="/create" className="mt-4 inline-block bg-green-500 text-white px-4 py-2 rounded">+ New Project</Link>
    </div>
  );
}