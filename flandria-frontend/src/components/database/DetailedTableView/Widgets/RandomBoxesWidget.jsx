import React from 'react';
import ListWidget, { ItemListWidgetItem } from './ListWidget';

const RandomBoxesWidget = ({ boxes }) => {
  if (!boxes.length >= 1) {
    return null;
  }

  return (
    <ListWidget
      label="Available In"
    >
      {boxes.map((box) => <ItemListWidgetItem key={box.code} tablename="random_box" item={box} />)}
    </ListWidget>
  );
};

export default RandomBoxesWidget;
