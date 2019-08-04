import React from "react";
import CardList from "../../shared/CardList";

export default class Description extends React.Component {
  render() {
    const {
      desc
    } = this.props;

    if (!desc) {
      return null;
    }

    return (
      <CardList header={true} padding={20}>
        <span className="card-title">Description</span>
        <span>{desc}</span>
      </CardList>
    )
  }
}