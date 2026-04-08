import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { getFarms, createFarm, updateFarm, deleteFarm, getDiseaseRisks, getReadings } from './api';
import './App.css';

function Dashboard() {
  const [farms, setFarms] = useState([]);
  const [risks, setRisks] = useState([]);
  const [stats, setStats] = useState({ readings: 0 });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    const farmsRes = await getFarms();
    const risksRes = await getDiseaseRisks();
    const readingsRes = await getReadings();
    setFarms(farmsRes.data);
    setRisks(risksRes.data);
    setStats({ readings: readingsRes.data.length });
  };

  const highRisks = risks.filter(r => r.risk_level === 'HIGH' && !r.is_resolved).length;
  const mediumRisks = risks.filter(r => r.risk_level === 'MEDIUM' && !r.is_resolved).length;

  return (
    <div className="dashboard">
      <h1><span className="logo-icon">🌱</span> FarmShield Dashboard</h1>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>{farms.length}</h3>
          <p>Farms</p>
        </div>
        <div className="stat-card warning">
          <h3>{stats.readings}</h3>
          <p>Sensor Readings</p>
        </div>
        <div className="stat-card danger">
          <h3>{highRisks}</h3>
          <p>High Risks</p>
        </div>
        <div className="stat-card medium">
          <h3>{mediumRisks}</h3>
          <p>Medium Risks</p>
        </div>
      </div>
      <h2>Farm Overview</h2>
      <div className="farm-grid">
        {farms.map(farm => (
          <div key={farm.id} className="farm-card">
            <h3>{farm.name}</h3>
            <p className="crop-type">{farm.crop_type}</p>
            <p>👤 {farm.owner}</p>
            <p>📍 {farm.location}</p>
            <p>📏 {farm.area_hectares} ha</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function Farms() {
  const [farms, setFarms] = useState([]);
  const [form, setForm] = useState({ name: '', owner: '', location: '', crop_type: 'VEGETABLES', area_hectares: 1 });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => { loadFarms(); }, []);

  const loadFarms = async () => {
    const res = await getFarms();
    setFarms(res.data);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (editingId) {
      await updateFarm(editingId, form);
    } else {
      await createFarm(form);
    }
    setForm({ name: '', owner: '', location: '', crop_type: 'VEGETABLES', area_hectares: 1 });
    setEditingId(null);
    loadFarms();
  };

  const handleEdit = (farm) => {
    setForm(farm);
    setEditingId(farm.id);
  };

  const handleDelete = async (id) => {
    if (confirm('Delete this farm?')) {
      await deleteFarm(id);
      loadFarms();
    }
  };

  return (
    <div className="page">
      <h1>🏡 Farms Management</h1>
      <form onSubmit={handleSubmit} className="form-card">
        <input placeholder="Farm Name" value={form.name} onChange={e => setForm({...form, name: e.target.value})} required />
        <input placeholder="Owner" value={form.owner} onChange={e => setForm({...form, owner: e.target.value})} required />
        <input placeholder="Location" value={form.location} onChange={e => setForm({...form, location: e.target.value})} required />
        <select value={form.crop_type} onChange={e => setForm({...form, crop_type: e.target.value})}>
          <option value="VEGETABLES">Vegetables</option>
          <option value="CACAO">Cacao</option>
          <option value="RICE">Rice</option>
          <option value="BANANA">Banana</option>
          <option value="CORN">Corn</option>
        </select>
        <input type="number" placeholder="Area (ha)" value={form.area_hectares} onChange={e => setForm({...form, area_hectares: e.target.value})} step="0.1" />
        <button type="submit">{editingId ? 'Update' : 'Add'} Farm</button>
        {editingId && <button type="button" onClick={() => {setEditingId(null); setForm({name:'',owner:'',location:'',crop_type:'VEGETABLES',area_hectares:1})}}>Cancel</button>}
      </form>
      <div className="farm-grid">
        {farms.map(farm => (
          <div key={farm.id} className="farm-card">
            <h3>{farm.name}</h3>
            <p className="crop-type">{farm.crop_type}</p>
            <p>👤 {farm.owner}</p>
            <p>📍 {farm.location}</p>
            <p>📏 {farm.area_hectares} ha</p>
            <div className="actions">
              <button onClick={() => handleEdit(farm)}>Edit</button>
              <button className="danger" onClick={() => handleDelete(farm.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function DiseaseRisks() {
  const [risks, setRisks] = useState([]);

  useEffect(() => { loadRisks(); }, []);

  const loadRisks = async () => {
    const res = await getDiseaseRisks();
    setRisks(res.data);
  };

  return (
    <div className="page">
      <h1>🦠 Disease Risk Analysis</h1>
      <table className="data-table">
        <thead>
          <tr>
            <th>Farm</th>
            <th>Disease</th>
            <th>Risk</th>
            <th>Probability</th>
            <th>Recommendation</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {risks.map(risk => (
            <tr key={risk.id}>
              <td>{risk.farm_name}</td>
              <td>{risk.disease_type}</td>
              <td><span className={`badge ${risk.risk_level.toLowerCase()}`}>{risk.risk_level}</span></td>
              <td>{(risk.probability * 100).toFixed(0)}%</td>
              <td>{risk.recommendation}</td>
              <td>{risk.is_resolved ? '✅ Resolved' : '⚠️ Active'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <nav className="sidebar">
          <h2>🌱 FarmShield</h2>
          <Link to="/">Dashboard</Link>
          <Link to="/farms">Farms</Link>
          <Link to="/disease">Disease Risks</Link>
        </nav>
        <main className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/farms" element={<Farms />} />
            <Route path="/disease" element={<DiseaseRisks />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;