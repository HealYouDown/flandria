import { css } from "styled-components";

const TileBase = css`
  background: linear-gradient(90deg,rgba(0,0,0,.5) 70%, transparent 110%);
  padding-top: 15px;
  padding-bottom: 15px;
  padding-left: 10px;
  padding-right: 10px;
  border-radius: 7px;
  cursor: pointer;

  &:hover {
    background: linear-gradient(90deg,rgba(0,0,0,.7) 70%, transparent 110%);

    .right-arrow path {
      fill: white;
    }
  }
`

export {
  TileBase
}