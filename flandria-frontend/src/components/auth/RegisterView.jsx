import Axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import { getApiUrl, setWindowTitle } from '../../helpers';
import AuthWrapper from './AuthWrapper';

const RegisterView = () => {
  const history = useHistory();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [fieldErrors, setFieldErrors] = useState([]);

  useEffect(() => {
    setWindowTitle('Sign Up');
  }, []);

  const onSubmit = async (event) => {
    setFieldErrors([]);
    event.preventDefault();

    // Check if all fields have some text in it
    const fields = [username, password, password2];
    let fieldsValid = true;
    fields.forEach((field) => {
      if (field.length === 0) {
        fieldsValid = false;
      }
    });
    if (!fieldsValid) {
      setFieldErrors(['Please fill out all fields.']);
      return null;
    }

    // Check if passwords match
    if (password !== password2) {
      setFieldErrors(['Passwords do not match.']);
      return null;
    }

    // Try to create a new user, if it fails, add error message.
    // If user was created without an error, redirec to login
    try {
      await Axios.post(`${getApiUrl()}/auth/register`, {
        username, password,
      });
      history.push('/auth/login');
    } catch (error) {
      const errorMessage = error.response.data.message;
      setFieldErrors([errorMessage]);
    }

    return null;
  };

  return (
    <AuthWrapper>
      <h2 className="text-2xl font-bold text-gray-900 md:text-5xl dark:text-white">Sign Up</h2>
      <form className="flex flex-col w-full gap-4" onSubmit={onSubmit}>
        <input
          className="text-input"
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="text-input"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <input
          className="text-input"
          type="password"
          placeholder="Password Confirm"
          value={password2}
          onChange={(e) => setPassword2(e.target.value)}
        />
        <div className="flex flex-col h-12 gap-2 overflow-auto text-red-400 dark:text-red-600 max-h-12">
          {fieldErrors.map((error) => <span key={error}>{error}</span>)}
        </div>
        <div className="flex justify-center">
          <button type="submit" className="px-16 py-2 text-xl font-semibold tracking-wider text-white uppercase bg-green-400 rounded-full outline-none dark:bg-green-600 focus-within:outline-none hover:bg-green-500 dark:hover:bg-green-500">
            Sign Up
          </button>
        </div>
      </form>
    </AuthWrapper>
  );
};

export default RegisterView;
