import React from 'react';
import { getEffectStrings } from '../../../../helpers';
import ListWidget from './ListWidget';

const EffectStatsWidget = ({ effects }) => {
  if (effects.length === 0) return null;

  return (
    <ListWidget
      label="Effects"
    >
      {getEffectStrings(effects).map((effectString) => (
        <div key={effectString} className="flex items-center px-4 py-2">
          <span className="text-gray-700 dark:text-white">{effectString}</span>
        </div>
      ))}
    </ListWidget>
  );
};

export default EffectStatsWidget;
