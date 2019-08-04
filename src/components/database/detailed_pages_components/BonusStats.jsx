import React from "react";
import getBonuses from "../../../constants/bonus_codes";
import CardList, { LabelValueListItem } from "../../shared/CardList";

export default class BonusStats extends React.Component {
  render() {
    const {
      data
    } = this.props;

    const bonuses = getBonuses(data);

    if (bonuses.length < 1) {
      return null;
    }

    return (
      <CardList header={true} list={true}>
        <span className="card-title">Bonus Stats</span>
        {bonuses.map((bonus, i) => {
          if (bonus["operator"] == "*")
            return (
              <LabelValueListItem 
                key={i}
                label={bonus["name"]}
                value={`${Math.round(bonus["value"]*100, 2)}%`} 
              />
            )
          
          return (
            <LabelValueListItem 
              key={i}
              label={bonus["name"]}
              value={bonus["operator"] + bonus["value"]}
            />
          )
        })}
      </CardList>
    )
  }
}