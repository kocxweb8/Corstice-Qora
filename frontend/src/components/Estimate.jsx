import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

export default function Estimate() {
  const { id } = useParams();
  const [estimate, setEstimate] = useState({});
  useEffect(() => {
    api.get(`/estimate/${id}`).then(res => setEstimate(res.data));
  }, [id]);
  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl mb-2">Estimate</h2>
      <div className="grid grid-cols-2 gap-2">
        <div>Material Cost:</div><div>{estimate.material_cost}</div>
        <div>Labour Cost:</div><div>{estimate.labour_cost}</div>
        <div>Equipment:</div><div>{estimate.equipment_cost}</div>
        <div>Overhead (10%):</div><div>{estimate.overhead}</div>
        <div>Tax (18%):</div><div>{estimate.tax}</div>
        <div>Contingency (5%):</div><div>{estimate.contingency}</div>
        <div className="font-bold">Grand Total:</div><div className="font-bold">{estimate.grand_total}</div>
      </div>
      <div className="mt-4">
        <button onClick={async () => {
          const res = await api.post(`/reports/${id}/generate?type=excel`);
          if (res.data.url) window.open(res.data.url);
        }} className="bg-blue-500 text-white px-4 py-2 rounded mr-2">Download Excel</button>
        <button onClick={async () => {
          const res = await api.post(`/reports/${id}/generate?type=pdf`);
          if (res.data.url) window.open(res.data.url);
        }} className="bg-red-500 text-white px-4 py-2 rounded">Download PDF</button>
      </div>
    </div>
  );
}