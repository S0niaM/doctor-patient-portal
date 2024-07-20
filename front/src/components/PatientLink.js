import React, { useState } from 'react';
import axios from 'axios';

function PatientLink({ onLinkSuccess }) {
  const [patientEmail, setPatientEmail] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/link_patient/', { patientEmail }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      onLinkSuccess();
      setPatientEmail('');
    } catch (error) {
      console.error('Error linking patient:', error);
    }
  };

  return (
    <div>
      <h3>Link Patient</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Patient Email"
          value={patientEmail}
          onChange={(e) => setPatientEmail(e.target.value)}
          required
        />
        <button type="submit">Link Patient</button>
      </form>
    </div>
  );
}

export default PatientLink;