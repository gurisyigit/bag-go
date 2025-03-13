import React from 'react';
import './ErrorMessage.css';
import errorIcon from '../icons/error.png';

interface ErrorMessageProps {
  message: string;
  className?: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, className }) => (
  <div id="error-message" className={`error-message d-flex align-items-center ${className}`}>
    <img src={errorIcon} alt="Error icon" className="error-icon me-2" />
    <div>
      <strong>Error</strong><br />
      {message}
    </div>
  </div>
);

export default ErrorMessage;
