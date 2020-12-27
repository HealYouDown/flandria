import React from 'react';
import ListWidget, { ItemListWidgetItem } from './ListWidget';

const RandomBoxContentWidget = ({ items }) => (
  <ListWidget
    label="Content"
  >
    {items.map((item) => (
      <ItemListWidgetItem
        key={item.item.code}
        tablename={item.item.table}
        item={item.item}
        subs={[`Qty. ${item.quantity}x`]}
      />
    ))}
  </ListWidget>
);

export default RandomBoxContentWidget;
