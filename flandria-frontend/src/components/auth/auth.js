import decode from 'jwt-decode';

const localStorageKey = 'ACCESS_TOKEN_FLANDRIA_V1.1';

function getToken() {
  return localStorage.getItem(localStorageKey) || null;
}

function isAuthenticated() {
  // Returns true if a token is found, however,
  // the token does not have to be valid.
  if (getToken()) {
    return true;
  }
  return false;
}

function loginUser(token) {
  localStorage.setItem(localStorageKey, token);
  window.dispatchEvent(new Event('storage'));
}

function logoutUser() {
  localStorage.removeItem(localStorageKey);
  window.dispatchEvent(new Event('storage'));
}

function getIdentity() {
  return decode(getToken()).identity;
}

export {
  isAuthenticated,
  getIdentity,
  loginUser,
  logoutUser,
};
