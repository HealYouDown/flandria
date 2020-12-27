import React from 'react';
import ListWidget, { ItemListWidgetItem, TextListWidgetItem } from './ListWidget';

const NPCShopItemsWidget = ({ items }) => (
  <ListWidget
    label="Shop"
  >
    {items.map((item) => (
      <ItemListWidgetItem
        key={item.item.code}
        tablename={item.item.table}
        item={item.item}
      />
    ))}
    {(items.length === 0) && (
      <TextListWidgetItem><span>This NPC does not sell any items.</span></TextListWidgetItem>
    )}
  </ListWidget>
);

export default NPCShopItemsWidget;
