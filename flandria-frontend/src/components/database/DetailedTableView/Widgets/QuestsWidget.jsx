import React from 'react';
import ListWidget, { ItemListWidgetItem } from './ListWidget';

const QuestsWidget = ({ quests, className, label = 'Quests' }) => {
  if (quests.length === 0) return null;

  return (
    <ListWidget
      className={className}
      label={label}
    >
      {quests.sort((a, b) => a.level < b.level).map((quest) => (
        <ItemListWidgetItem
          key={quest.code}
          tablename="quest"
          item={quest}
        />
      ))}
    </ListWidget>
  );
};

export default QuestsWidget;
