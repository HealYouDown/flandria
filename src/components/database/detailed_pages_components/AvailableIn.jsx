import React from "react";
import CardList, { ClickableListItem } from "../../shared/CardList";
import Icon from "../Icon";
import Name from "../Name";

export default class AvailableIn extends React.Component {
  render() {
    const {
      randomBoxes
    } = this.props;

    if (randomBoxes.length < 1) {
      return null;
    }

    return (
      <CardList header={true} list={true}>
        <span className="card-title">Available In</span>
        {randomBoxes.map((box, i) => {
          return (
            <ClickableListItem key={i} hover={false} link={`/database/random_box/${box.code}`} >
              <Icon table="random_box" data={box} />
              <Name table="random_box" data={box} />
            </ClickableListItem>
          )
        })}
      </CardList>
    )
  }
}