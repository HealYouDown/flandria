import React from "react";
import CardList, { ClickableListItem } from "../../shared/CardList";
import Name from "../Name";
import Icon from "../Icon";

export default class NeededFor extends React.Component {
  render() {
    const {
      recipeData,
      secondJobData
    } = this.props;

    if (recipeData.length == 0 && secondJobData.length == 0) {
      return null;
    }

    return (
      <CardList header={true} list={true}>
        <span className="card-title">Needed for</span>
        {recipeData.map((recipe, i) => {
          return (
            <ClickableListItem key={i} hover={false} link={`/database/recipe/${recipe.code}`}>
              <Icon table="recipe" data={recipe} />
              <Name table="recipe" data={recipe} />
            </ClickableListItem>
          )
        })}
        {secondJobData.map((productBook, i) => {
          return (
            <ClickableListItem key={i} hover={false} link={`/database/product_book/${productBook.code}`}>
              <Icon table="recipe" data={productBook} />
              <Name table="recipe" data={productBook} />
            </ClickableListItem>
          )
        })}
      </CardList>
    )
  }
}