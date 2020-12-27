import React from 'react';
import ListWidget, { ItemListWidgetItem, TextListWidgetItem } from './ListWidget';

function sortDrops(a, b) {
  if (a.monster.rating.value > b.monster.rating.value) return -1;
  if (a.monster.rating.value < b.monster.rating.value) return 1;

  if (a.monster.level > b.monster.level) return -1;
  if (a.monster.level < b.monster.level) return 1;

  if (a.monster.name > b.monster.name) return 1;
  if (a.monster.name < b.monster.name) return -1;

  return 1;
}

const DroppedByWidget = ({ droppedBy }) => {
  const uniqueDrops = droppedBy.filter(
    (v, i, a) => a.findIndex((t) => t.monster.code === v.monster.code) === i,
  );

  return (
    <ListWidget
      label="Dropped By"
    >
      {uniqueDrops.sort(sortDrops).map((drop) => (
        <ItemListWidgetItem
          key={drop.monster.code}
          tablename="monster"
          item={drop.monster}
        />
      ))}
      {(droppedBy.length === 0) && (
      <TextListWidgetItem><span>No monsters found.</span></TextListWidgetItem>
      )}
    </ListWidget>
  );
};

export default DroppedByWidget;
