import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: { 'Content-Type': 'application/json' }
});

// Farm CRUD
export const getFarms = () => api.get('/farms/');
export const getFarm = (id) => api.get(`/farms/${id}/`);
export const createFarm = (data) => api.post('/farms/', data);
export const updateFarm = (id, data) => api.put(`/farms/${id}/`, data);
export const deleteFarm = (id) => api.delete(`/farms/${id}/`);

// Sensor Readings
export const getReadings = () => api.get('/readings/');
export const getFarmReading = (id) => api.get(`/farms/${id}/latest_reading/`);

// Disease Risks
export const getDiseaseRisks = () => api.get('/disease-risks/');
export const getActiveRisks = () => api.get('/disease-risks/active/');

// Irrigation
export const getIrrigations = () => api.get('/irrigation/'); // placeholder

// API Cheatcode:
// GET    /api/farms/       -> list farms
// POST   /api/farms/       -> create farm
// GET    /api/farms/{id}/  -> get farm
// PUT    /api/farms/{id}/  -> update farm
// DELETE /api/farms/{id}/  -> delete farm

export default api;