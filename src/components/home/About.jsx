import React from "react";
import { Row, Col } from "react-grid-system";
import Card, { CardHeader, CardBody } from "../common/Card";

const About = () => {
  document.title = "About";

  return (
    <Row justify="center">
      <Col md={6}>
        <Card>
          <CardHeader>
            <span className="card-title">About</span>
          </CardHeader>
          <CardBody>
            <p>Hi. My name is Jeremy and I'm the developer of Flandria! :)</p>

            <p>
              Flandria is a project that started late in 2018 and was launched starting in the new year 2019.
              Even today, Flandria is still in active development and changes very frequently.
            </p>

            <p>If you've got any questions, feel free to concact me.</p>

            <p>
              E-Mail: healyoudown[at]gmail.com
              <br/>
              Discord: Jeremy#8813
            </p>
          </CardBody>
        </Card>
      </Col>
    </Row>
  )
}

export default About;