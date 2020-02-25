import React from "react";
import Background from "./Background";
import Nav from "./Nav";
import Footer from "./Footer";
import Container from "./Container";

const Layout = (props) => {
  return (
    <>
      <Nav />
      <Container>{props.children}</Container>
      <Footer />
      <Background />
    </>
  )
}

export default Layout;