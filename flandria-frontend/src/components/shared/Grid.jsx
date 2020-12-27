import React from 'react';

const Column = ({
  children, sm = 12, md, lg, xl, xl2, gap = 'gap-4',
}) => {
  let className = `col-span-${sm}`;

  if (md) className += ` md:col-span-${md}`;
  if (lg) className += ` lg:col-span-${lg}`;
  if (xl) className += ` xl:col-span-${xl}`;
  if (xl2) className += ` 2xl:col-span-${xl2}`;

  return (
    <div className={`${className} ${gap} flex flex-col`}>
      {children}
    </div>
  );
};

const Grid = ({ children, gap = 'gap-4', className }) => (
  <div className={`grid grid-cols-12 ${gap} ${className}`}>
    {children}
  </div>
);

export default Grid;
export {
  Column,
};
