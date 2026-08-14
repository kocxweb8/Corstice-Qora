import React, { useEffect, useRef, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

export default function DrawingViewer() {
  const { id } = useParams();
  const canvasRef = useRef(null);
  const [entities, setEntities] = useState([]);
  useEffect(() => {
    api.get(`/drawings/${id}/entities`).then(res => setEntities(res.data));
  }, [id]);
  useEffect(() => {
    if (!canvasRef.current || entities.length === 0) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const scale = 0.05;
    entities.forEach(ent => {
      const geom = ent.geometry;
      if (ent.entity_type === 'line') {
        ctx.beginPath();
        ctx.moveTo(geom.start[0]*scale + 50, geom.start[1]*scale + 50);
        ctx.lineTo(geom.end[0]*scale + 50, geom.end[1]*scale + 50);
        ctx.strokeStyle = 'blue';
        ctx.stroke();
      } else if (ent.entity_type === 'block') {
        ctx.fillStyle = 'red';
        ctx.fillRect(geom.insert[0]*scale + 50, geom.insert[1]*scale + 50, 5, 5);
      }
    });
  }, [entities]);
  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl mb-2">Drawing Viewer</h2>
      <canvas ref={canvasRef} width={800} height={600} className="border"></canvas>
      <div className="mt-2">
        <button onClick={() => window.location.href=`/project/${id}/detected`} className="bg-blue-500 text-white px-4 py-2 rounded">Detect Objects</button>
      </div>
    </div>
  );
}