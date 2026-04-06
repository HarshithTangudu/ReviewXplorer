import React from 'react';
import { AlertTriangle } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message }) => {
  return (
    <div className="card error-card glow-border-red">
      <p className="error-text">
        <AlertTriangle size={20} /> {message}
      </p>
    </div>
  );
};

export default ErrorMessage;
