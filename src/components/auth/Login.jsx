import React from "react";
import AuthService from "../AuthService";
import { Redirect } from "react-router";
import { Link } from "react-router-dom";
import CardList from "../shared/CardList";
import { Row, Col } from "react-grid-system";

import "../../styles/forms.css";

export default class Login extends React.Component {
  constructor(props) {
    super(props);

    this.auth = new AuthService();

    this.state = {
      username: "",
      password: "",
      error: false,
      errorMessage: "",
    }
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  componentDidMount() {
    document.title = "Login";
  }

  handleSubmit(event) {
    event.preventDefault();
    const {
      username,
      password
    } = this.state;

    this.auth.login(username, password)
    .then(res => {
      if (res["error"]) {
        this.setState({
          error: true,
          errorMessage: res.errorMessage
        })
      }
      else {
        this.setState({
          error: false, errorMessage: ""
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
      error,
      errorMessage
    } = this.state;

    if (this.auth.loggedIn()) {
      return <Redirect to="/" />
    }

    return (
      <Row justify="center">
        <Col md={4}>
          <CardList header={true}>
            <span className="card-title card-title-center">Login</span>
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
                <label className="form-input-label">Password</label>
                <input className="form-input input-style" type="password" name="password" value={password} onChange={this.handleChange} />
              </div>
              <div className="form-input-group align-right">
                <button type="submit">Log in</button>
              </div>
            </form>
            <div style={{paddingBottom: "25px", marginLeft: "15px"}}>
              <span>New User? <Link style={{color: "white"}} to="/auth/register">Register here!</Link></span>
            </div>
          </CardList>
        </Col>
      </Row>
    )
  }
}
