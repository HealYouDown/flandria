import React from 'react';
import { resolveLandClassNames, resolveSeaClassNames } from '../../helpers';
import { weaponTables, armorTables, shipTables } from '../../constants';

const ItemSubs = ({ tablename, item, additionalSubs = [] }) => {
  const subs = [...additionalSubs];

  if (item) {
    if (tablename === 'guild') {
      subs.push(...[
        `${item.server.name}`,
      ]);
      // Only add those if the value exist. Search does not display
      // all of them, so they are undefined by default.
      if (item.member_count) subs.push(`${item.member_count} Member`);
      if (item.avg_level_land) subs.push(`Avg. Level ${item.avg_level_land.toFixed(2)}`);
    } else if (tablename === 'player') {
      subs.push(...[
        `${item.character_class.name}`,
        `${item.level_land}/${item.level_sea}`,
        `#${item.rank}`,
      ]);
    } else if (tablename === 'monster') {
      subs.push(...[
        `Lv. ${item.level}`,
        `${item.rating.name}`,
        `${item.area.name}`,
      ]);
    } else if (tablename === 'quest') {
      subs.push(...[
        `Lv. ${item.level}`,
        `${item.area.name}`,
      ]);

      if (item.class) {
        subs.push(resolveLandClassNames(item.class));
      }
    } else if (tablename === 'essence') {
      subs.push(...[
        `Lv. ${item.required_weapon_level}`,
        item.is_core_essence ? 'Core' : 'Meta',
        `${item.equip_type.name}`,
      ]);
    } else if (tablename === 'npc') {
      subs.push(...[
        `Lv. ${item.level}`,
      ]);
    } else if (['hat', 'dress', 'accessory'].includes(tablename)) {
      subs.push(...[
        `Lv. ${item.level_land}/${item.level_sea}`,
        `${item.gender.name}`,
        `${resolveLandClassNames(item.class_land)}`,
      ]);
    } else if (weaponTables.includes(tablename) || armorTables.includes(tablename)) {
      subs.push(...[
        `Lv. ${item.level_land}/${item.level_sea}`,
        `${resolveLandClassNames(item.class_land)}`,
      ]);
    } else if (shipTables.includes(tablename)) {
      subs.push(...[
        `Lv. ${item.level_sea}`,
        `${resolveSeaClassNames(item.class_sea)}`,
      ]);
    }
  }

  return (
    <div className="flex flex-row flex-wrap">
      {subs.map((sub, index) => (
        <span key={sub} className="text-sm leading-4 text-gray-500 dark:text-white dark:text-opacity-70">
          {sub}
          {((index + 1) < subs.length) && (<span className="px-1">•</span>)}
        </span>
      ))}
    </div>
  );
};

export default ItemSubs;
