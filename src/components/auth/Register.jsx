import React, {useState} from "react";
import Card, { CardHeader, CardBody } from "../common/Card";
import { Row, Col } from "react-grid-system";
import { TextInput, InputWrapper, InputLabel, ConfirmButton } from "../common/Inputs";
import { toast } from 'react-toastify';
import history from "../history";


const Register = () => {
  document.title = "Register";

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password1, setPassword1] = useState("");
  const [password2, setPassword2] = useState("");

  const register = (event) => {
    event.preventDefault();
  
    if (password1 != password2) {
      toast.error("Passwords do not match.");
      return;
    }

    let res;
    fetch("/api/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({username, email, password: password1})
    })
    .then(fetchResponse => {
      res = fetchResponse;
      return fetchResponse.json()
    })
    .then(json => {
      if (!res.ok) {
        toast.error(json.msg);
      }
      else {
        toast.success(json.msg);
        history.push("/auth/login");
      }
    })
  }

  return (
    <Row justify="center">
      <Col md={4}>
        <Card>
          <CardHeader>
            <span className="card-title">Register</span>
          </CardHeader>
          <CardBody>
            <form onSubmit={register}>
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
                <InputLabel>E-Mail</InputLabel>
                <TextInput
                  fontsize={16}
                  type="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                />
              </InputWrapper>
              <InputWrapper>
                <InputLabel>Password</InputLabel>
                <TextInput
                  fontsize={16}
                  type="password"
                  value={password1}
                  onChange={e => setPassword1(e.target.value)}
                />
              </InputWrapper>
              <InputWrapper>
                <InputLabel>Password confirmation</InputLabel>
                <TextInput
                  fontsize={16}
                  type="password"
                  value={password2}
                  onChange={e => setPassword2(e.target.value)}
                />
              </InputWrapper>
              <InputWrapper>
                <ConfirmButton type="submit">Register</ConfirmButton>
              </InputWrapper>
            </form>
          </CardBody>
        </Card>
      </Col>
    </Row>
  )
}

export default Register;