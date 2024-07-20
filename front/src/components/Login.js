import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { FaUser, FaEnvelope, FaLock, FaStethoscope } from 'react-icons/fa';
import './Login.css';

function Login() {
  const [isLogin, setIsLogin] = useState(true);
  const [isDoctor, setIsDoctor] = useState(true); // New state for doctor/patient toggle
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [specialty, setSpecialty] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let endpoint;
      let data;
      
      if (isLogin) {
        endpoint = isDoctor ? '/api/login/doctor/' : '/api/login/patient/';
        data = { email, password };
      } else {
        endpoint = isDoctor ? '/api/register/doctor/' : '/api/register/patient/';
        data = isDoctor ? { name, email, password, specialty } : { name, email, password };
      }
      
      const response = await axios.post(`http://localhost:8000${endpoint}`, data);
      localStorage.setItem('token', response.data.token);
      navigate('/dashboard');
    } catch (error) {
      console.error('Error:', error.response ? error.response.data : error.message);
    }
  };

  return (
    <div className="login-container">
      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="login-box"
      >
        <h2>{isLogin ? 'Login' : 'Register'}</h2>
        <form onSubmit={handleSubmit}>
          {!isLogin && (
            <>
              <div className="input-group">
                <FaUser />
                <input
                  type="text"
                  placeholder="Name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
              {isDoctor && !isLogin && (
                <div className="input-group">
                  <FaStethoscope />
                  <input
                    type="text"
                    placeholder="Specialty"
                    value={specialty}
                    onChange={(e) => setSpecialty(e.target.value)}
                    required
                  />
                </div>
              )}
            </>
          )}
          <div className="input-group">
            <FaEnvelope />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <FaLock />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="submit-btn"
            type="submit"
          >
            {isLogin ? 'Login' : 'Register'}
          </motion.button>
        </form>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="toggle-btn"
          onClick={() => setIsLogin(!isLogin)}
        >
          {isLogin ? 'Need to register?' : 'Already have an account?'}
        </motion.button>
        {!isLogin && (
          <div className="role-toggle">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className={`toggle-btn ${isDoctor ? 'active' : ''}`}
              onClick={() => setIsDoctor(true)}
            >
              Register as Doctor
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className={`toggle-btn ${!isDoctor ? 'active' : ''}`}
              onClick={() => setIsDoctor(false)}
            >
              Register as Patient
            </motion.button>
          </div>
        )}
      </motion.div>
    </div>
  );
}

export default Login;
