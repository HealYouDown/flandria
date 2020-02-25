import React, {useState} from "react";
import Card, { CardHeader, CardBody } from "../common/Card";
import { Row, Col } from "react-grid-system";
import { TextInput, InputWrapper, InputLabel, ConfirmButton } from "../common/Inputs";
import { toast } from 'react-toastify';
import history from "../history";
import { loginUser, isLoggedIn } from "./auth";
import { Link } from "react-router-dom";


const Login = () => {
  document.title = "Login";

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  if (isLoggedIn()) {
    history.push("/");
  };

  const login = (event) => {
    event.preventDefault();

    let res;
    fetch("/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({username, password})
    })
    .then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json();
    })
    .then(json => {
      if (!res.ok) {
        toast.error(json.msg);
      }
      else {
        loginUser(json.access_token);
        history.push("/");
      }
    })
  }

  return (
    <Row justify="center">
      <Col md={4}>
        <Card>
          <CardHeader>
            <span className="card-title">Login</span>
          </CardHeader>
          <CardBody>
            <form onSubmit={login}>
              <InputWrapper>
                <InputLabel>Username</InputLabel>
                <TextInput
                  fontsize={16}
                  type="text"
                  value={username}
                  onChange={e => setUsername(e.target.value)}
                />
              </InputWrapper>
              <InputWrapper>
                <InputLabel>Password</InputLabel>
                <TextInput
                  fontsize={16}
                  type="password"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                />
              </InputWrapper>
              <InputWrapper>
                <ConfirmButton type="submit">Login</ConfirmButton>
              </InputWrapper>
            </form>
            <br />
            <span>New User? <Link to="/auth/register">Register here!</Link></span>
          </CardBody>
        </Card>
      </Col>
    </Row>
  )
}

export default Login;