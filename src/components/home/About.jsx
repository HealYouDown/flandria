import React from "react";
import CardList from "../shared/CardList";
import { Row, Col } from "react-grid-system";

const About = () => {
  return (
    <Row justify="center">
      <Col md={7}>
        <CardList header={true} padding={20}>
          <span className="card-title card-title-center">About</span>
          <span>
            Flandria is a fan project and is in no way related to the publisher of Florensia (GiikuGames).
          </span>

          <br />
          <br />
          
          <span>
            <b>Contact Details</b>
            <br />
            <span>E-Mail: healyoudown[at]gmail.com</span>
            <br />
            <span>Discord: Jeremy#8813</span>
            <br />
            <span>Bergruen: Shadow</span>
            <br />
            <span>LuxPlena: HealYouDown</span>
          </span>
        </CardList>
      </Col>
    </Row>
  )
}

export default About;