import decode from 'jwt-decode';

const KEY = "access_token_1"

const getToken = () => {
  return localStorage.getItem(KEY) || null;
}

const isLoggedIn = () => {
  if (getToken()) {
    return true;
  }
  return false;
}

const loginUser = (token) => {
  localStorage.setItem(KEY, token);
  window.dispatchEvent(new Event("storage"));
}

const logoutUser = () => {
  localStorage.removeItem(KEY);
  window.dispatchEvent(new Event("storage"));
}

const getDecodedToken = () => {
  // Using jwt-decode npm package to decode the token
  return decode(getToken());
}

const getId = () => {
  if (isLoggedIn()) {
    return getDecodedToken().identity.id;
  }
  return null;
}

const getName = () => {
  if (isLoggedIn()) {
    return getDecodedToken().identity.username;
  }
  return false;
}

const getCanEditDrops = () => {
  if (isLoggedIn()) {
    return getDecodedToken().identity.can_edit_drops;
  }
  return false;
}

export {
  getToken,
  isLoggedIn,
  loginUser,
  logoutUser,
  getId,
  getName,
  getCanEditDrops,
}