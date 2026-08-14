import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

export default function BOQ() {
  const { id } = useParams();
  const [boq, setBoq] = useState([]);
  useEffect(() => {
    api.get(`/boq/${id}`).then(res => setBoq(res.data));
  }, [id]);
  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl mb-2">Bill of Quantities</h2>
      <table className="w-full border">
        <thead><tr><th>Description</th><th>Qty</th><th>Unit</th><th>Rate</th><th>Amount</th></tr></thead>
        <tbody>
          {boq.map(item => (
            <tr key={item.id}><td>{item.description}</td><td>{item.quantity}</td><td>{item.unit}</td><td>{item.rate}</td><td>{item.amount}</td></tr>
          ))}
        </tbody>
      </table>
      <div className="mt-4">
        <button onClick={() => window.location.href=`/project/${id}/estimate`} className="bg-green-500 text-white px-4 py-2 rounded">Calculate Estimate</button>
      </div>
    </div>
  );
}