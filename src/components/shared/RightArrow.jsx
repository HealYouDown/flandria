import React from "react";
import { FaAngleRight } from "react-icons/fa";

export default class RightArrow extends React.Component {
  render() {
    return (
      <div className="arrow-box" style={{flexGrow: 0, alignSelf: "center"}}>
        <i>
          <FaAngleRight fontSize={20} style={{verticalAlign: "middle"}} />
        </i>
      </div>
    )
  }
}