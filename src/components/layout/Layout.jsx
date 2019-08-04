import React from "react";
import { Container } from "react-grid-system";
import ErrorBoundary from "./ErrorBoundary";
import Header from "./Header";
import Footer from "./Footer";
import Background from "./Background";

import "./Layout.css";

export default class Layout extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      backgroundImage: "/static/img/backgrounds/background-image.jpeg"
    }
  }
  render() {
    return (
      <>
        <Header />

        <main>
          <Container fluid style={{height: "100%"}}>
            <ErrorBoundary>
              {this.props.children}
            </ErrorBoundary>
          </Container>
        </main>

        <Footer />

      <Background />
    </>
    )
  }
}
