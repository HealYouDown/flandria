import React from 'react';
import ListWidget, { ItemListWidgetItem } from './ListWidget';

const SoldByWidget = ({ soldBy }) => {
  if (soldBy.length === 0) return null;

  return (
    <ListWidget
      label="Sold by"
    >
      {soldBy.map((npc) => <ItemListWidgetItem key={npc.code} tablename="npc" item={npc} />)}
    </ListWidget>
  );
};

export default SoldByWidget;
