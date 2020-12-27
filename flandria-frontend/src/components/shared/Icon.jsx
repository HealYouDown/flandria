import React, { useState } from 'react';
import { getImagePath } from '../../helpers';

const monsterMapping = {
  '-1': 'border-gray-200 dark:border-dark-4',
  0: 'border-gray-200 dark:border-dark-4',
  1: 'border-monster-grade-1',
  2: 'border-monster-grade-2',
  3: 'border-monster-grade-3',
};

const itemMapping = {
  '-1': 'border-gray-200 dark:border-dark-4',
  0: 'border-item-grade-0',
  1: 'border-item-grade-1',
  2: 'border-item-grade-2',
  3: 'border-item-grade-3',
};

const Icon = ({
  icon, className = '', alt = '', tablename, rareGrade = -1,
}) => {
  const [error, setError] = useState(false);

  if ((tablename === 'quest') || error) {
    return null;
  }

  // Image Path
  let imagePathSuffix;
  switch (tablename) {
    case 'monster':
      imagePathSuffix = 'monster_icons';
      break;
    case 'npc':
      imagePathSuffix = 'npc_icons';
      break;
    case 'skill':
      imagePathSuffix = 'skill_icons';
      break;
    default:
      imagePathSuffix = 'item_icons';
  }
  const src = getImagePath(`${imagePathSuffix}/${icon}`);

  // Border Color
  let borderColor = 'border-gray-200 dark:border-dark-4';
  if (tablename === 'monster') {
    borderColor = monsterMapping[rareGrade];
  } else {
    borderColor = itemMapping[rareGrade];
  }

  return (
    <img
      onError={() => setError(true)}
      className={`rounded-full border-3 border-opacity-50 ${borderColor} ${className}`}
      src={src}
      alt={alt}
    />
  );
};

export default Icon;
