import React from 'react';
import './InputField.css';
import userIcon from '../icons/user.png';
import emailIcon from '../icons/email.png';
import passwordIcon from '../icons/password.png';

const iconMap: { [key: string]: string } = {
  user: userIcon,
  email: emailIcon,
  password: passwordIcon,
};

interface InputFieldProps {
  type: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder: string;
  iconName: string;
}

const InputField: React.FC<InputFieldProps> = ({ type, name, value, onChange, placeholder, iconName }) => {
  const iconSrc = iconMap[iconName];

  return (
    <div id="input-field" className="input-field">
      {iconSrc && <img src={iconSrc} alt={`${iconName} icon`} className="input-icon" />}
      <input
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required
      />
    </div>
  );
}

export default InputField;
