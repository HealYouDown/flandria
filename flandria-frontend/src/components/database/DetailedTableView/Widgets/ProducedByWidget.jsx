import React from 'react';
import ListWidget, { ItemListWidgetItem } from './ListWidget';

const ProducedByWidget = ({ recipes, productions }) => {
  if (!recipes.length >= 1 && !productions.length >= 1) {
    return null;
  }

  return (
    <ListWidget
      label="Produced by"
    >
      {recipes.map((recipe) => <ItemListWidgetItem key={recipe.code} tablename="recipe" item={recipe} />)}
      {productions.map((production) => <ItemListWidgetItem key={production.code} tablename="production" item={production} />)}
    </ListWidget>
  );
};

export default ProducedByWidget;
