import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

export default function Quantities() {
  const { id } = useParams();
  const [quantities, setQuantities] = useState({});
  useEffect(() => {
    api.get(`/quantities/${id}`).then(res => setQuantities(res.data));
  }, [id]);
  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl mb-2">Quantity Takeoff</h2>
      <table className="w-full border">
        <thead><tr><th>Item</th><th>Gross</th><th>Deduction</th><th>Net</th><th>Unit</th></tr></thead>
        <tbody>
          {Object.entries(quantities).map(([key, val]) => (
            <tr key={key}><td>{key}</td><td>{val.gross}</td><td>{val.deduction}</td><td>{val.net}</td><td>{val.unit}</td></tr>
          ))}
        </tbody>
      </table>
      <div className="mt-4">
        <button onClick={() => window.location.href=`/project/${id}/boq`} className="bg-blue-500 text-white px-4 py-2 rounded">Generate BOQ</button>
      </div>
    </div>
  );
}