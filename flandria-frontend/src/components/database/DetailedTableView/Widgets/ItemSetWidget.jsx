import React from 'react';
import ListWidget, { ItemListWidgetItem } from './ListWidget';
import EffectItemSubs from '../../../shared/EffectItemSubs';

const ItemSetWidget = ({ itemSet }) => {
  if (!itemSet) return null;

  return (
    <ListWidget
      label="Itemset"
      subItem={<EffectItemSubs effects={itemSet.effects} />}
    >
      {itemSet.items.map((item) => (
        <ItemListWidgetItem
          key={item.code}
          tablename={item.table}
          item={item}
        />
      ))}
    </ListWidget>
  );
};

export default ItemSetWidget;
