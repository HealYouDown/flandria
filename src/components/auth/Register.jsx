import React from "react";
import AuthService from "../AuthService";
import { Redirect } from "react-router";
import { Link } from "react-router-dom";
import CardList from "../shared/CardList";
import { Row, Col } from "react-grid-system";

import "../../styles/forms.css";

export default class Register extends React.Component {
  constructor(props) {
    super(props);

    this.auth = new AuthService();

    this.state = {
      username: "",
      email: "",
      password: "",
      password2: "",
      accountCreated: false,
      error: false,
      errorMessage: "",
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    document.title = "Register";
  }

  handleSubmit(event) {
    event.preventDefault();
    const {
      username,
      email,
      password,
      password2,
    } = this.state;

    if (password != password2) {
      this.setState({
        error: true,
        errorMessage: "Passwords do not match."
      })
      return;
    }

    this.auth.register(username, email, password)
    .then(res => {
      if (res["error"]) {
        this.setState({
          error: true,
          errorMessage: res.errorMessage
        })
      }
      else {
        this.setState({
          error: false, errorMessage: "", accountCreated: true
        })
      }
    })
  }

  handleChange(event) {
    this.setState({
      [event.target.name]: event.target.value
    })
  }

  render() {
    const {
      username,
      password,
      password2,
      email,
      accountCreated,
      error,
      errorMessage
    } = this.state;

    if (accountCreated) {
      return <Redirect to="/auth/login" />
    }

    return (
      <Row justify="center">
        <Col md={4}>
          <CardList header={true}>
            <span className="card-title card-title-center">Register</span>
            <form onSubmit={this.handleSubmit}>
              {error && (
                <div className="form-input-group">
                  <span style={{color: "red"}}>{errorMessage}</span>
                </div>
              )}
              <div className="form-input-group">
                <label className="form-input-label">Username</label>
                <input className="form-input input-style" type="text" name="username" value={username} onChange={this.handleChange} />
              </div>
              <div className="form-input-group">
                <label className="form-input-label">E-Mail</label>
                <input className="form-input input-style" type="email" name="email" value={email} onChange={this.handleChange} />
              </div>
              <div className="form-input-group">
                <label className="form-input-label">Password</label>
                <input className="form-input input-style" type="password" name="password" value={password} onChange={this.handleChange} />
              </div>
              <div className="form-input-group">
                <label className="form-input-label">Password confirm</label>
                <input className="form-input input-style" type="password" name="password2" value={password2} onChange={this.handleChange} />
              </div>
              <div className="form-input-group align-right">
                <button type="submit">Register</button>
              </div>
            </form>
          </CardList>
        </Col>
      </Row>
    )
  }
}
