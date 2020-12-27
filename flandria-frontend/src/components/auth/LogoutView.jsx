import { useEffect } from 'react';
import { useHistory } from 'react-router-dom';
import { logoutUser } from './auth';

const LogoutView = () => {
  const history = useHistory();

  useEffect(() => {
    logoutUser();
    history.push('/');
  }, []);

  return null;
};

export default LogoutView;
