import decode from 'jwt-decode';
import request from "superagent";

const apiUrl = document.location.protocol + "//" + document.location.hostname + ":" + document.location.port + "/api/v1/";

export default class AuthService {
  constructor() {
    this.login = this.login.bind(this);
    this.getProfile = this.getProfile.bind(this);
    this.fetch = this.fetch.bind(this);
  }

  fetch(method, url, options={}) {
    const {
      body,
      query
    } = options;

    return request(method, apiUrl + url)
      .set('Accept', 'application/json')
      .set("Authorization", "Bearer " + this.getToken())
      .send(body)
      .query(query)
      .then(res => res)
      .catch(err => {
        if (err.response.body.error == "ExpiredAccessError") {
          this.logout();
          return this.fetch(method, url, options);
        }
        else {
          return {error: true, errorMessage: err.response.body.message}
        }
      })
  }

  login(username, password) {
    return request
      .post(apiUrl + "auth/login")
      .send({username, password})
      .then(res => {
        this.setToken(res.body.access_token); // Setting the token in localStorage
        window.dispatchEvent(new Event("storage"))
        return {error: false};
      })
      .catch(err => {
        return {error: true, errorMessage: err.response.body.message}
      })
  }

  register(username, email, password) {
    return request
      .post(apiUrl + "auth/register")
      .send({username, email, password})
      .then(res => res)
      .catch(err => {
        return {error: true, errorMessage: err.response.body.message}
      })
  }

  logout() {
    // Clear user token and profile data from localStorage
    localStorage.removeItem('id_token');
    window.dispatchEvent(new Event("storage"));
  }

  loggedIn() {
    // Checks if there is a saved token and it's still valid
    const token = this.getToken() // Getting token from localstorage
    return !!token && !this.isTokenExpired(token) // handwaiving here
  }

  isTokenExpired(token) {
    try {
      const decoded = decode(token);
      if (decoded.exp < Date.now() / 1000) { // Checking if token is expired.
        return true;
      }
      else
        return false;
    }
    catch (err) {
      return false;
    }
  }

  setToken(idToken) {
    // Saves user token to localStorage
    localStorage.setItem('id_token', idToken)
  }

  getToken() {
    // Retrieves the user token from localStorage
    return localStorage.getItem('id_token') || ""
  }

  getProfile() {
    // Using jwt-decode npm package to decode the token
    return decode(this.getToken());
  }

  getId() {
    return this.getProfile()["id"];
  }

  getUsername() {
    return this.getProfile()["username"];
  }

  isAdmin() {
    if (!this.loggedIn()) {
      return false;
    }
    return this.getProfile()["admin"];
  }

  canEditDrops() {
    if (!this.loggedIn()) {
      return false;
    }
    return this.getProfile()["can_edit_drops"];
  }

}
