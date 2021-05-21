import React from 'react';

const IconGroup = ({
  icons, size = 'w-8 h-8', space = '-space-x-2',
}) => (
  <div className={`flex ${space}`}>
    {icons.map((icon) => <img key={icon} className={`inline-block rounded-full border-2 border-gray-200 dark:border-dark-4 ${size}`} src={icon} alt="" />)}
  </div>
);

export default IconGroup;
