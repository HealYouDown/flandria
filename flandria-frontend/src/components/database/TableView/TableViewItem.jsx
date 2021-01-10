import React from 'react';
import { Link } from 'react-router-dom';
import { getRareGradeFromItem } from '../../../helpers';
import EffectItemSubs from '../../shared/EffectItemSubs';
import Icon from '../../shared/Icon';
import ItemDuration from '../../shared/ItemDuration';
import ItemSubs from '../../shared/ItemSubs';

const TableViewItem = ({ tablename, item, showIcon = true }) => {
  let iconName = item.icon;
  let iconTablename = tablename;
  let itemName = item.name;
  let rareGrade = getRareGradeFromItem(tablename, item);
  let subsTablename = tablename;
  let subsItem = item;
  let link = `/database/${tablename}/${item.code}`;

  if (tablename === 'production') {
    const resultItem = item.result_item;

    iconName = resultItem.icon;
    iconTablename = resultItem.table;
    itemName = resultItem.name;
    rareGrade = getRareGradeFromItem(resultItem.table, resultItem);
    subsTablename = resultItem.table;
    subsItem = resultItem.item_data;
  } else if (tablename === 'quest') {
    itemName = item.title;
  } else if (tablename === 'guild') {
    // Somehow react router is only able to decode % in url if it is
    // encoded twice.
    // Thanks to the guilds with % in their name...
    link = encodeURI(encodeURI(`/ranking/guilds/${item.name}`));
  }

  return (
    <Link
      to={link}
      className="flex flex-row items-center px-4 py-2 rounded-md cursor-pointer dark:from-dark-3 hover:bg-gradient-to-r from-gray-200 to-transparent hover:animate-scale group"
    >
      {showIcon && (
      <Icon
        tablename={iconTablename}
        className="group-hover:border-opacity-100 w-10 h-10 mr-1.5 box-content"
        icon={iconName}
        rareGrade={rareGrade}
      />
      )}
      <div className="flex flex-col justify-center">
        <h3 className="font-semibold leading-none text-gray-700 dark:text-white">
          {itemName}
          <ItemDuration duration={item.duration} />
        </h3>
        <ItemSubs tablename={subsTablename} item={subsItem} />
        {item.effects && (
          <EffectItemSubs effects={item.effects} />
        )}
      </div>
    </Link>
  );
};

export default TableViewItem;
