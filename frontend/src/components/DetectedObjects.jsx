import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

export default function DetectedObjects() {
  const { id } = useParams();
  const [objects, setObjects] = useState([]);
  useEffect(() => {
    api.post(`/analysis/${id}/detect`).then(res => {
      setObjects(res.data);
    });
  }, [id]);
  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl mb-2">Detected Objects</h2>
      <table className="w-full border">
        <thead><tr><th>Type</th><th>Confidence</th><th>Layer</th><th>Verified</th></tr></thead>
        <tbody>
          {objects.map(obj => (
            <tr key={obj.id}><td>{obj.object_type}</td><td>{obj.confidence}</td><td>{obj.properties?.layer}</td><td>{obj.verified ? 'Yes' : 'No'}</td></tr>
          ))}
        </tbody>
      </table>
      <div className="mt-4">
        <button onClick={() => window.location.href=`/project/${id}/quantities`} className="bg-green-500 text-white px-4 py-2 rounded">Calculate Quantities</button>
      </div>
    </div>
  );
}