import Axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import { getApiUrl, setWindowTitle } from '../../helpers';
import { loginUser } from './auth';
import AuthWrapper from './AuthWrapper';

const LoginView = () => {
  const history = useHistory();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fieldErrors, setFieldErrors] = useState([]);

  useEffect(() => {
    setWindowTitle('Sign In');
  }, []);

  const onSubmit = async (event) => {
    setFieldErrors([]);
    event.preventDefault();

    // Check if all fields have some text in it
    const fields = [username, password];
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

    // Request a JWT token
    // Redirect to the home page on success
    try {
      const resp = await Axios.post(`${getApiUrl()}/auth/login`, {
        username, password,
      });
      loginUser(resp.data.access_token);
      history.push('/');
    } catch (error) {
      const errorMessage = error.response.data.message;
      setFieldErrors([errorMessage]);
    }

    return null;
  };

  return (
    <AuthWrapper>
      <h2 className="text-2xl font-bold text-gray-900 md:text-5xl dark:text-white">Sign In</h2>
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
        <div className="flex flex-col h-12 gap-2 overflow-auto text-red-400 dark:text-red-600 max-h-12">
          {fieldErrors.map((error) => <span key={error}>{error}</span>)}
        </div>
        <div className="flex justify-center">
          <button type="submit" className="px-16 py-2 text-xl font-semibold tracking-wider text-white uppercase bg-green-400 rounded-full outline-none dark:bg-green-600 focus-within:outline-none hover:bg-green-500 dark:hover:bg-green-500">
            Sign In
          </button>
        </div>
      </form>
    </AuthWrapper>
  );
};

export default LoginView;
