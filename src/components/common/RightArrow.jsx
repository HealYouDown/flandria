import React from "react";
import styled from "styled-components";

const RightArrowWrapper = styled.svg`
  height: 20px;
  align-self: center;

  & path {
    fill: #aaa;
    transition: fill 0.15s;
  }
`

const RightArrow = () => {
  return (
    <RightArrowWrapper className="right-arrow" viewBox="0 0 256 512">
      <path 
        d="M224.3 273l-136 136c-9.4 9.4-24.6 9.4-33.9 0l-22.6-22.6c-9.4-9.4-9.4-24.6 0-33.9l96.4-96.4-96.4-96.4c-9.4-9.4-9.4-24.6 0-33.9L54.3 103c9.4-9.4 24.6-9.4 33.9 0l136 136c9.5 9.4 9.5 24.6.1 34z"
      />
    </RightArrowWrapper>
  )
}

export default RightArrow;