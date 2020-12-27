import React from 'react';
import ListWidget, { ItemListWidgetItem } from './ListWidget';

const MaterialList = ({
  resultItem, materials, label = 'Materials', showResultItem = true,
}) => (
  <>
    {showResultItem && (
    <ListWidget label="Result Item">
      <ItemListWidgetItem
        tablename={resultItem.table}
        item={resultItem}
      />
    </ListWidget>
    )}
    <ListWidget
      label={label}
    >
      {materials.map((materialObj) => (
        <ItemListWidgetItem
          key={materialObj.item.code}
          tablename={materialObj.item.table}
          item={materialObj.item}
          subs={[`Qty. ${materialObj.quantity}x`]}
        />
      ))}
    </ListWidget>
  </>
);

export default MaterialList;
