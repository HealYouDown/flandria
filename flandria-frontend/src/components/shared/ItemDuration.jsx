import React from 'react';
import { getDurationString } from '../../helpers';

const ItemDuration = ({ duration, className = '' }) => {
  if (!duration) return null;

  return (
    <span className={`ml-1 font-semibold leading-none text-gray-500 dark:text-white dark:text-opacity-70 ${className}`}>
      {getDurationString(duration)}
    </span>
  );
};
export default ItemDuration;
