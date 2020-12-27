import React from 'react';
import ListWidget, { ItemListWidgetItem } from './ListWidget';

const QuestRewardsWidget = ({ rewards, selectCount }) => {
  if (rewards.length === 0) return null;

  return (
    <ListWidget
      label={`Rewards (Select ${selectCount}/${rewards.length})`}
    >
      {rewards.map((item) => (
        <ItemListWidgetItem
          key={item.item.code}
          tablename={item.item.table}
          item={item.item}
          subs={[`Qty. ${item.amount}x`]}
        />
      ))}

    </ListWidget>
  );
};

export default QuestRewardsWidget;
