/* eslint-disable no-unused-vars */
import React from 'react';
import Select from 'react-select';
import {
  armorTables, effectCodes, shipTables, weaponTables,
} from '../../../constants';

const SelectLabel = ({ children }) => (
  <span className="px-2 py-2 text-lg font-semibold leading-5 tracking-wide text-gray-700 dark:text-white">{children}</span>
);

const FilterMenu = ({
  tablename, filter, setFilter,
}) => {
  const updateFilter = (key, value, resetPage) => {
    const newFilterMap = { ...filter };
    newFilterMap[key] = value;

    if (resetPage) {
      newFilterMap.page = 1;
    }

    setFilter(newFilterMap);
  };

  const tablesWithAreaFilter = ['monster', 'quest'];
  const tablesWithEffectFilter = ['dress', 'hat', 'accessory', 'essence'];

  // Order options (always the same)
  const orderOptions = [
    { value: 'asc', label: 'Ascending' },
    { value: 'desc', label: 'Descending' },
  ];

  // Sort options
  const sortOptions = [
    { label: 'Added', value: 'index' },
    { label: 'Name', value: 'name' },
  ];
  if (tablename === 'monster') {
    sortOptions.push(...[
      { label: 'Level', value: 'level' },
      { label: 'HP', value: 'hp' },
      { label: 'Experience', value: 'experience' },
      { label: 'Min. Dmg', value: 'minimal_damage' },
      { label: 'Max. Dmg', value: 'maximal_damage' },
    ]);
  } else if (tablename === 'essence') {
    sortOptions.push(...[
      { label: 'Item Lv.', value: 'level_land' },
    ]);
  } else if (tablename === 'quest') {
    sortOptions.push(...[
      { label: 'Level', value: 'level' },
    ]);
  } else if (tablename === 'accessory') {
    sortOptions.push(...[
      { label: 'Level', value: 'level_land' },
    ]);
  } else if (weaponTables.includes(tablename) || armorTables.includes(tablename)) {
    sortOptions.push(...[
      { label: 'Land Level', value: 'level_land' },
      { label: 'Sea Level', value: 'level_sea' },
    ]);
  }

  // Filter Options
  const filterOptions = [
    { label: 'All', value: 'all' },
  ];
  if (tablename === 'monster') {
    filterOptions.push(...[
      { label: 'Normal', value: 'rating:0' },
      { label: 'Elite', value: 'rating:1' },
      { label: 'Mini-Boss', value: 'rating:2' },
      { label: 'Boss', value: 'rating:3' },
    ]);
  } else if (weaponTables.includes(tablename) || armorTables.includes(tablename)) {
    filterOptions.push(...[
      { label: 'Noble', value: 'class_land:N' },
      { label: 'Magic Knight', value: 'class_land:K' },
      { label: 'Court Magician', value: 'class_land:M' },
      { label: 'Mercenary', value: 'class_land:W' },
      { label: 'Gladiator', value: 'class_land:G' },
      { label: 'Guardian Swordman', value: 'class_land:D' },
      { label: 'Saint', value: 'class_land:S' },
      { label: 'Priest', value: 'class_land:P' },
      { label: 'Shaman', value: 'class_land:A' },
      { label: 'Explorer', value: 'class_land:E' },
      { label: 'Excavator', value: 'class_land:B' },
      { label: 'Sniper', value: 'class_land:H' },
    ]);
  } else if (tablename === 'essence') {
    filterOptions.push(...[
      { label: 'Meta Essence', value: 'core_essence:0' },
      { label: 'Core Essence', value: 'core_essence:1' },
      { label: 'Equip: All', value: 'essence_equip:0' },
      { label: 'Equip: Weapons', value: 'essence_equip:1' },
      { label: 'Equip: Armor', value: 'essence_equip:2' },
    ]);
  } else if (tablename === 'production') {
    filterOptions.push(...[
      { label: 'Weapon Smith', value: 'production:0' },
      { label: 'Armor Smith', value: 'production:1' },
      { label: 'Alchemist', value: 'production:2' },
      { label: 'Workmanship', value: 'production:3' },
      { label: 'Essence', value: 'production:4' },
    ]);
  } else if (shipTables.includes(tablename)) {
    filterOptions.push(...[
      { label: 'Armored Ship', value: 'class_sea:A' },
      { label: 'Big Gun Ship', value: 'class_sea:G' },
      { label: 'Torpedo Ship', value: 'class_sea:H' },
      { label: 'Mainteance Ship', value: 'class_sea:M' },
      { label: 'Assault Ship', value: 'class_sea:R' },
    ]);
  } else if (tablename === 'accessory') {
    filterOptions.push(...[
      { label: 'Necklace', value: 'accessory:0' },
      { label: 'Earring', value: 'accessory:1' },
      { label: 'Ring', value: 'accessory:2' },
    ]);
  }

  // Area options
  const areaOptions = [
    { label: 'Land & Sea', value: '-1' },
    { label: 'Land', value: '0' },
    { label: 'Sea', value: '1' },
  ];

  return (
    <div className="grid grid-cols-1 gap-3 mt-4 md:grid-cols-2 lg:grid-cols-3">
      <div className="flex flex-col">
        <SelectLabel>Order</SelectLabel>
        <Select
          classNamePrefix="react-select"
          options={orderOptions}
          value={orderOptions.filter((opt) => opt.value === filter.order)}
          onChange={(option) => updateFilter('order', option.value)}
        />
      </div>
      <div className="flex flex-col">
        <SelectLabel>Sort</SelectLabel>
        <Select
          classNamePrefix="react-select"
          options={sortOptions}
          value={sortOptions.filter((opt) => opt.value === filter.sort)}
          onChange={(option) => updateFilter('sort', option.value)}
        />
      </div>
      {filterOptions.length > 1 && (
        <div className="flex flex-col">
          <SelectLabel>Filter</SelectLabel>
          <Select
            classNamePrefix="react-select"
            options={filterOptions}
            value={filterOptions.filter((opt) => opt.value === filter.filter)}
            onChange={(option) => updateFilter('filter', option.value, true)}
          />
        </div>
      )}
      {tablesWithAreaFilter.includes(tablename) && (
        <div className="flex flex-col">
          <SelectLabel>Area</SelectLabel>
          <Select
            classNamePrefix="react-select"
            options={areaOptions}
            value={areaOptions.filter((opt) => opt.value === filter.area)}
            onChange={(option) => updateFilter('area', option.value, true)}
          />
        </div>
      )}
      {tablesWithEffectFilter.includes(tablename) && (
      <div className="flex flex-col">
        <SelectLabel>Effects</SelectLabel>
        <Select
          classNamePrefix="react-select"
          options={effectCodes.filter((effectCodeOpt) => effectCodeOpt.label)}
          value={effectCodes.filter((opt) => {
            try {
              return JSON.parse(filter.effects).includes(opt.value);
            } catch (e) {
              return null;
            }
          })}
          onChange={(options) => {
            const selectedEffectCodes = [];
            if (options) {
              options.forEach((opt) => selectedEffectCodes.push(opt.value));
            }
            updateFilter('effects', JSON.stringify(selectedEffectCodes), true);
          }}
          isMulti
        />
      </div>
      )}
    </div>
  );
};

export default FilterMenu;
