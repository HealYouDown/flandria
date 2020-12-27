/* eslint-disable prefer-destructuring */
import React from 'react';
import { Link } from 'react-router-dom';
import Card, { CardHeader, CardHeaderTitle } from '../../../shared/Card';
import Icon from '../../../shared/Icon';
import ItemSubs from '../../../shared/ItemSubs';

const ItemListWidgetItem = ({ tablename, item, subs }) => {
  let name = '';
  let rareGrade = 0;
  let icon = '';
  switch (tablename) {
    case 'quest':
      name = item.title;
      rareGrade = -1;
      break;
    case 'monster':
      name = item.name;
      icon = item.icon;
      rareGrade = item.rating.value;
      break;
    case 'production':
      name = item.result_item.name;
      icon = item.result_item.icon;
      rareGrade = item.result_item.rare_grade;
      break;
    default:
      name = item.name;
      icon = item.icon;
      rareGrade = item.rare_grade || -1;
  }

  const link = (item.code === 'money') ? '#' : `/database/${tablename}/${item.code}`;

  return (
    <Link
      to={link}
      className="flex flex-row items-center justify-start px-4 py-2 cursor-pointer group hover:bg-gray-200 dark:hover:bg-dark-4"
    >
      <Icon
        className="mr-1.5 w-10 h-10 group-hover:border-opacity-100"
        tablename={tablename}
        icon={icon}
        rareGrade={rareGrade}
      />
      <div className="flex flex-col">
        <span className="text-gray-700 dark:text-white group-hover:text-gray-900 dark:group-hover:text-white">
          {name}
        </span>
        <ItemSubs
          tablename={tablename}
          // Monster and Quests have their sub data in the item object, not in item_data
          // like ItemList objects have.
          item={(['quest', 'monster'].includes(tablename)) ? item : item.item_data}
          additionalSubs={subs}
        />
      </div>
    </Link>
  );
};

const TextListWidgetItem = ({ children }) => (
  <p className="px-4 py-2 text-gray-700 whitespace-pre-line dark:text-white dark:text-opacity-70">
    {children}
  </p>
);

const ListWidget = ({
  label, subItem, children, className,
}) => (
  <Card
    className={className}
    header={(
      <CardHeader>
        <CardHeaderTitle>{label}</CardHeaderTitle>
        {subItem}
      </CardHeader>
    )}
  >
    <div className="overflow-y-auto divide-y divide-gray-200 max-h-112 dark:divide-dark-4">
      {children}
    </div>
  </Card>
);

export default ListWidget;
export {
  ItemListWidgetItem, TextListWidgetItem,
};
