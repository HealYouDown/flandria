import React from "react";
import CardList, { ClickableListItem } from "../../shared/CardList";
import Icon from "../Icon";
import Name from "../Name";

export default class DroppedBy extends React.Component {
  render() {
    const {
      droppedBy
    } = this.props;

    if (droppedBy.length < 1) {
      return null;
    }

    return (
      <CardList header={true} list={true}>
        <span className="card-title">Dropped by</span>
        {droppedBy.map((monster, i) => {
          return (
            <ClickableListItem key={i} hover={false} link={`/database/monster/${monster.code}`}>
              <Icon table="monster" data={monster} />
              <Name table="monster" data={monster} />
            </ClickableListItem>
          )
        })}
      </CardList>
    )
  }
}