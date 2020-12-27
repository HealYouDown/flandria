/* eslint-disable no-unused-vars */
import React, { useState } from 'react';
import { armorTables, weaponTables } from '../../../../constants';
import Card, { CardHeader, CardHeaderTitle } from '../../../shared/Card';

const LabelValueItem = ({ label, value, isUpgraded }) => (
  <div className="flex flex-row justify-between px-4 py-2 text-gray-700 dark:text-white">
    <span className="font-semibold">{label}</span>
    <span className={isUpgraded ? 'text-green-500 dark:text-green-400' : ''}>
      {value}
      {isUpgraded}
    </span>
  </div>
);

const UpgradeWidget = ({ tablename, obj, upgradeData }) => {
  const [upgradeLevel, setUpgradeLevel] = useState(0);

  const getUpgradeRuleValue = (num) => upgradeData[upgradeLevel].effects[`effect_${num}`].value;

  // If an item is upgradable, it should have 16 rows with data.
  if (upgradeData.length !== 16) {
    return null;
  }

  const children = [];

  if (weaponTables.includes(tablename)) {
    const phMin = obj.minimal_physical_attack;
    const phMax = obj.maximal_physical_attack;
    const mgMin = obj.minimal_magic_attack;
    const mgMax = obj.maximal_magic_attack;
    const attackSpeed = obj.attack_speed;
    const attackRange = obj.attack_range;

    // All Items have a 'Physical Damage' stat, but just for some it changes when upgrading.
    const isPhUpgradable = ['rapier', 'dagger', 'one_handed_sword', 'two_handed_sword', 'rifle', 'duals'].includes(tablename);
    const phIncrease = isPhUpgradable ? getUpgradeRuleValue(0) : 0;
    const newPhMin = Math.floor(phMin + phIncrease);
    const newPhMax = Math.floor(phMax + phIncrease);
    children.push(
      <LabelValueItem
        label="Physical Damage"
        key="ph-dmg"
        value={`${newPhMin} ~ ${newPhMax}`}
        isUpgraded={isPhUpgradable && (upgradeLevel >= 1)}
      />,
    );

    // Magical Damage
    const valueNum = (tablename === 'cariad') ? 1 : 2;
    const mgIncrease = getUpgradeRuleValue(valueNum);
    const newMgMin = Math.floor(mgMin + mgIncrease);
    const newMgMax = Math.floor(mgMax + mgIncrease);
    children.push(
      <LabelValueItem
        label="Magical Damage"
        key="magic-dmg"
        value={`${newMgMin} ~ ${newMgMax}`}
        isUpgraded={
          ['cariad', 'rapier', 'dagger'].includes(tablename)
          && (upgradeLevel >= 1)
        }
      />,
    );

    // Attack Speed
    children.push(
      <LabelValueItem
        label="Attack Speed"
        key0="akt-speed-weapon"
        value={`${attackSpeed / 1000}s`}
        isUpgraded={false}
      />,
    );

    // Range
    children.push(
      <LabelValueItem
        label="Attack Range"
        key="akt-range"
        value={`${attackRange}m`}
        isUpgraded={false}
      />,
    );
  } else if (armorTables.includes(tablename)) {
    const phDef = obj.physical_defense;
    const mgDef = obj.magic_defense;

    // Ph Def Coat
    const coatPhIncrease = (tablename === 'coat') ? getUpgradeRuleValue(0) : 0;
    const newPhDef = Math.floor(phDef + coatPhIncrease);
    children.push(
      <LabelValueItem
        label="Physical Defense"
        key="ph-def"
        value={`${newPhDef}`}
        isUpgraded={(tablename === 'coat') && (upgradeLevel >= 1)}
      />,
    );

    // Mg Def Coat
    const pantsMgIncrease = (tablename === 'pants') ? getUpgradeRuleValue(0) : 0;
    const newMgDef = Math.floor(mgDef + pantsMgIncrease);
    children.push(
      <LabelValueItem
        label="Magical Defense"
        key="mg-def"
        value={`${newMgDef}`}
        isUpgraded={(tablename === 'pants') && (upgradeLevel >= 1)}
      />,
    );

    if (tablename === 'gauntlet') {
      const hitrate = Math.floor(getUpgradeRuleValue(0));
      children.push(...[
        <LabelValueItem
          label="Hitrate"
          key="hitrate"
          value={hitrate}
          isUpgraded={upgradeLevel >= 1}
        />,
        <LabelValueItem
          label="Attack Speed"
          key="akt-speed"
          value={`${upgradeLevel}%`}
          isUpgraded={upgradeLevel >= 1}
        />,
      ]);
    } else if (tablename === 'shoes') {
      const avoidance = Math.floor(getUpgradeRuleValue(0));
      children.push(...[
        <LabelValueItem
          label="Avoidance"
          key="avoidance"
          value={avoidance}
          isUpgraded={upgradeLevel >= 1}
        />,
        <LabelValueItem
          label="Moving Speed"
          key="move-speed"
          value={`${upgradeLevel}%`}
          isUpgraded={upgradeLevel >= 1}
        />,
      ]);
    }
  }

  return (
    <Card
      header={(
        <CardHeader>
          <CardHeaderTitle>Upgrade</CardHeaderTitle>
        </CardHeader>
    )}
    >
      <div className="divide-y divide-gray-200 dark:divide-dark-4">
        <div className="flex flex-row items-center gap-2 px-4 py-2">
          <span className="text-gray-700 dark:text-white">{upgradeLevel}</span>
          <input
            className="flex-grow"
            type="range"
            value={upgradeLevel}
            min={0}
            max={15}
            onChange={(e) => setUpgradeLevel(parseInt(e.target.value, 10))}
          />
        </div>
        {children}
      </div>
    </Card>
  );
};

export default UpgradeWidget;
