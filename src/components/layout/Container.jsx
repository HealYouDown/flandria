import React from "react";
import styled from "styled-components";

const Main = styled.main`
  padding: 35px 50px;
`

const Container = (props) => {

  return (
    <Main>
      {props.children}
    </Main>
  )
}

export default Container;