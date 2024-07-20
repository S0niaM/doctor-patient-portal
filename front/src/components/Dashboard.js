import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PDFUpload from './PDFUpload';
import PatientLink from './PatientLink';
import './Dashboard.css'; // Assuming you'll create this CSS file

function Dashboard() {
  const [doctor, setDoctor] = useState(null);
  const [pdfs, setPdfs] = useState([]);
  const [patients, setPatients] = useState([]);

  useEffect(() => {
    fetchPDFs();
    fetchPatients();
  }, []);

  const fetchPDFs = async () => {
    try {
      const response = await axios.get('/api/upload_pdf/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setPdfs(response.data);
    } catch (error) {
      console.error('Error fetching PDFs:', error);
    }
  };

  const fetchPatients = async () => {
    try {
      const response = await axios.get('/api/link_patient/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setPatients(response.data);
    } catch (error) {
      console.error('Error fetching patients:', error);
    }
  };

  const linkPatient = async (patientEmail) => {
    try {
      const response = await axios.post('/api/link_patient/', { patient_email: patientEmail }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      console.log(response.data);
      fetchPatients();
    } catch (error) {
      console.error('Error linking patient:', error);
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome, Dr. {doctor?.name}</h1>
      </header>
      <main className="dashboard-main">
        <section className="dashboard-section">
          <h2>Upload PDF</h2>
          <PDFUpload onUploadSuccess={fetchPDFs} />
        </section>
        <section className="dashboard-section">
          <h2>Link Patient</h2>
          <PatientLink onLinkSuccess={fetchPatients} />
        </section>
      </main>
    </div>
  );
}

export default Dashboard;