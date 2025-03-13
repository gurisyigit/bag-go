// components/Register/Register.tsx
import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link component from react-router-dom
import InputField from './InputField';
import ErrorMessage from './ErrorMessage';
import './Register.css';

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [errors, setErrors] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setErrors({ ...errors, confirmPassword: 'Passwords do not match' });
      return;
    }

    // If no errors, proceed with form submission
    console.log(formData);
  };

  return (
    <div id="register-page">
      <div className="main-section">
        <div className="header">BagAndGo</div>
        <form className="register-form w-100" onSubmit={handleSubmit}>
          <h2 className="text-center mb-4">Register</h2>

          <InputField
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Enter your name"
            iconName="user"
          />

          <InputField
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter your email"
            iconName="email"
          />

          {errors.email && (
            <ErrorMessage message={errors.email} className="registration-error" />
          )}

          <InputField
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            iconName="password"
          />

          <InputField
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            placeholder="Confirm your password"
            iconName="password"
          />

          {errors.confirmPassword && (
            <ErrorMessage message={errors.confirmPassword} className="registration-error" />
          )}

          <button type="submit" className="btn btn-primary w-100">
            Register
          </button>

          
        </form>
        {/* Add the "Already have an account?" text and clickable link */}
        <div className="text-center mt-3">
            Already have an account?{' '}
            <Link to="/login" className="login-link">
              Log in
            </Link>
          </div>
      </div>
    </div>
  );
};

export default Register;
