import React from 'react';
import { formatTextLinebreaks } from '../../../../helpers';
import ListWidget, { TextListWidgetItem } from './ListWidget';

const DescriptionWidget = ({ description, label = 'Description' }) => {
  if (!description) return null;

  return (
    <ListWidget
      label={label}
    >
      <TextListWidgetItem>
        {formatTextLinebreaks(description)}
      </TextListWidgetItem>
    </ListWidget>
  );
};

export default DescriptionWidget;
