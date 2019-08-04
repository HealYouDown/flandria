import React from "react";
import "./Name.css";

export default class Name extends React.Component {
  render() {
    const {
      table,
      data,
      normalProductBookColor
    } = this.props;

    if (table == "monster") {
      let rating = data.rating_type
      // Monster
      return (
        <span className={`monster-rating rating-${rating}`}>
          {data.name}
        </span>
      )
    }
    else {
      var rareGrade = data.rare_grade;
      if (table == "product_book" && !normalProductBookColor) { 
        // Product book only has the result item rare grade in overview.
        rareGrade = data.target.result_item.rare_grade;
      }
      return (
        <span className={`item-rare-grade rare-grade-${rareGrade}`}>
          {data.name}
          {data.duration && data.duration != -1 && (
            <span className="item-duration"> {data.duration}D</span>
          )}
        </span>
      )
    }
  }
}