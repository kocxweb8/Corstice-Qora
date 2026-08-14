import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import ProjectList from './components/ProjectList';
import ProjectCreate from './components/ProjectCreate';
import DrawingUpload from './components/DrawingUpload';
import DrawingViewer from './components/DrawingViewer';
import DetectedObjects from './components/DetectedObjects';
import Quantities from './components/Quantities';
import BOQ from './components/BOQ';
import Estimate from './components/Estimate';
import api from './api';

function App() {
  const [projects, setProjects] = useState([]);

  useEffect(() => {
    api.get('/projects').then(res => setProjects(res.data));
  }, []);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-100">
        {/* Navbar with Qora SVG Logo */}
        <nav className="bg-blue-700 p-4 text-white flex items-center gap-4 shadow-md">
          <Link to="/" className="flex items-center gap-2">
            <img src="/qora-logo.svg" alt="Qora Logo" className="h-10 w-10 object-contain" />
            <span className="font-bold text-2xl tracking-wide">Qora</span>
          </Link>
          <span className="text-sm opacity-80 hidden sm:block">Draw.Measure.Estimate.</span>
          <div className="flex-1"></div>
          <Link to="/projects" className="hover:underline">Projects</Link>
          <Link to="/create" className="hover:underline bg-blue-500 px-3 py-1 rounded">+ New</Link>
        </nav>

        <div className="container mx-auto p-4">
          <Routes>
            <Route path="/" element={<ProjectList projects={projects} />} />
            <Route path="/projects" element={<ProjectList projects={projects} />} />
            <Route path="/create" element={<ProjectCreate onProjectCreated={() => window.location.href='/projects'} />} />
            <Route path="/project/:id" element={<DrawingUpload />} />
            <Route path="/project/:id/viewer" element={<DrawingViewer />} />
            <Route path="/project/:id/detected" element={<DetectedObjects />} />
            <Route path="/project/:id/quantities" element={<Quantities />} />
            <Route path="/project/:id/boq" element={<BOQ />} />
            <Route path="/project/:id/estimate" element={<Estimate />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;