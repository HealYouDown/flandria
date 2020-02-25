import React from "react";
import styled from "styled-components";
import breakpoint from "../breakpoint";

const VisibleWrapper = styled.div`
  display: none;
  ${props => breakpoint(props.bp)`
    display: block;
  `}
`

const HiddenWrapper = styled.div`
  display: block;
  ${props => breakpoint(props.bp)`
    display: none;
  `}
`

const Visible = (props) => {
  return (
    <VisibleWrapper bp={props.breakpoint}>
      {props.children}
    </VisibleWrapper>
  )
}

const Hidden = (props) => {
  return (
    <HiddenWrapper bp={props.breakpoint}>
      {props.children}
    </HiddenWrapper>
  )
}

export {Visible, Hidden};