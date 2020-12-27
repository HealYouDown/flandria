import React from 'react';
import { getEffectStrings } from '../../helpers';

const EffectItemSubs = ({ effects }) => {
  const effectStrings = getEffectStrings(effects);

  return (
    <div className="flex flex-row flex-wrap">
      {effectStrings.map((effect, index) => (
        <span key={effect} className="text-xs leading-4 text-blue-500 text-opacity-90 dark:text-blue-300 dark:text-opacity-90">
          {effect}
          {((index + 1) < effectStrings.length) && (<span className="px-1">•</span>)}
        </span>
      ))}
    </div>
  );
};

export default EffectItemSubs;
