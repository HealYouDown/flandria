import React from "react";
import styled from "styled-components";
import breakpoint from "../breakpoint";

const Main = styled.main`
  padding: 35px 20px;

  ${breakpoint("md")`
    padding: 35px 50px;
  `}
`

const Container = (props) => {

  return (
    <Main>
      {props.children}
    </Main>
  )
}

export default Container;