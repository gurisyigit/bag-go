import React, { useState } from 'react';
import InputField from '../Register/InputField'; // Reuse the InputField component
import ErrorMessage from '../Register/ErrorMessage'; // Reuse the ErrorMessage component
import { Link } from 'react-router-dom'; // Import Link component from react-router-dom
import './Login.css';

const Login: React.FC = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const [errors, setErrors] = useState({
    email: '',
    password: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    
    let formIsValid = true;
    const newErrors = { email: '', password: '' };

    // Check if email is absent
    if (!formData.email) {
      newErrors.email = 'Email is required';
      formIsValid = false;
    }

    // Check if password is absent
    if (!formData.password) {
      newErrors.password = 'Password is required';
      formIsValid = false;
    }

    setErrors(newErrors);

    // Proceed with form submission if valid
    if (formIsValid) {
      console.log('Logged in:', formData);
    }
  };

  return (
    <div id="login-page">
      <div className="main-section">
        <div className="header">BagAndGo</div>
        <form className="login-form w-100" onSubmit={handleSubmit}>
          <h2 className="text-center mb-4">Login</h2>

          
          <InputField
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Enter your email"
            iconName="email"
          />
          {errors.email && (
            <ErrorMessage message={errors.email} className="login-error" />
          )}

          <InputField
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Enter your password"
            iconName="password"
          />
          {errors.password && (
            <ErrorMessage message={errors.password} className="login-error" />
          )}

          <button type="submit" className="btn btn-primary w-100">
            Login
          </button>
        </form>
        <div className="text-center mt-3">
            Don't have an account?{' '}
            <Link to="/register" className="register-link">
              Register
            </Link>
          </div>
      </div>
    </div>
  );
};

export default Login;
