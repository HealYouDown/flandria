import React from 'react';
import { getRareGradeFromItem, tablenameToTitle } from '../../../helpers';
import Breadcrumbs from '../../shared/Breadcrumbs';
import Icon from '../../shared/Icon';

const DetailedTableViewHeader = ({ tablename, item }) => {
  let iconName = item.icon;
  let iconTablename = tablename;
  let itemName = item.name;
  let rareGrade = getRareGradeFromItem(tablename, item);

  if (tablename === 'production') {
    const resultItem = item.result_item;

    iconName = resultItem.icon;
    iconTablename = resultItem.table;
    itemName = resultItem.name;
    rareGrade = getRareGradeFromItem(resultItem.table, resultItem);
  } else if (tablename === 'quest') {
    itemName = item.title;
  }

  return (
    <div className="flex flex-col pb-3 border-b border-gray-200 dark:border-dark-3">
      <div>
        <Breadcrumbs
          items={[
            { text: 'Items', url: '/database' },
            { text: tablenameToTitle(tablename), url: `/database/${tablename}` },
            { text: itemName, url: `/database/${tablename}/${item.code}` },
          ]}
        />
        <div className="flex items-center mt-2">
          <Icon
            icon={iconName}
            tablename={iconTablename}
            rareGrade={rareGrade}
            className="w-10 h-10 mr-1.5 box-content border-opacity-100"
          />
          <h2 className="mt-0 text-2xl font-semibold text-gray-700 md:text-3xl dark:text-white">
            {itemName}
          </h2>
        </div>
      </div>
    </div>
  );
};

export default DetailedTableViewHeader;
