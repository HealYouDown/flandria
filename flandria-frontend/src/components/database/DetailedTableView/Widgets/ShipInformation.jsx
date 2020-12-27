import React from 'react';
import Card, { CardHeader, CardHeaderTitle } from '../../../shared/Card';

const ShipInformation = ({ tablename, obj }) => {
  const labels = [];

  if (tablename === 'ship_body') {
    labels.push(...[
      { label: 'Physical Defense', value: Number(obj.physical_defense).toLocaleString() },
      { label: 'Protection', value: Number(obj.protection).toLocaleString() },
      { label: 'DP', value: Number(obj.dp).toLocaleString() },
      { label: 'Guns Front', value: obj.guns_front },
      { label: 'Guns Side', value: obj.guns_side },
      { label: 'Crew Size', value: obj.crew_size },
    ]);
  } else if (tablename === 'ship_front') {
    labels.push(...[
      { label: 'Physical Defense', value: Number(obj.physical_defense).toLocaleString() },
      { label: 'Protection', value: Number(obj.protection).toLocaleString() },
      { label: 'DP', value: Number(obj.dp).toLocaleString() },
      { label: 'Balance', value: obj.balance },
    ]);
  } else if (tablename === 'ship_head_mast') {
    labels.push(...[
      { label: 'Favorable Wind', value: Number(obj.favorable_wind).toLocaleString() },
      { label: 'Adverse Wind', value: Number(obj.adverse_wind).toLocaleString() },
      { label: 'Turning Power', value: Number(obj.turning_power).toLocaleString() },
      { label: 'Balance', value: obj.balance },
    ]);
  } else if (tablename === 'ship_main_mast') {
    labels.push(...[
      { label: 'Favorable Wind', value: Number(obj.favorable_wind).toLocaleString() },
      { label: 'Adverse Wind', value: Number(obj.adverse_wind).toLocaleString() },
      { label: 'Turning Power', value: Number(obj.turning_power).toLocaleString() },
      { label: 'Acceleration', value: obj.acceleration },
      { label: 'Deceleration', value: obj.deceleration },
      { label: 'Balance', value: obj.balance },
    ]);
  } else if (tablename === 'ship_figure') {
    labels.push(...[
      { label: 'Protection', value: obj.protection },
      { label: 'Balance', value: obj.balance },
    ]);
  } else if (tablename === 'ship_magic_stone') {
    labels.push(...[
      { label: 'EN', value: Number(obj.en).toLocaleString() },
      { label: 'EN Recovery', value: Number(obj.en_recovery).toLocaleString() },
      { label: 'Balance', value: obj.balance },
    ]);
  } else if (tablename === 'ship_anchor') {
    labels.push(...[
      { label: 'Turning Power', value: obj.turning_power },
      { label: 'Deceleration', value: obj.deceleration },
      { label: 'Balance', value: obj.balance },
    ]);
  } else if (tablename === 'ship_normal_weapon') {
    labels.push(...[
      { label: 'Damage', value: Number(obj.damage).toLocaleString() },
      { label: 'Range', value: `${obj.range}m` },
      { label: 'Critical', value: `${obj.critical}%` },
      { label: 'Reloadspeed', value: `${obj.reloadspeed}s` },
      { label: 'Hit range', value: `${obj.hitrange}m` },
      { label: 'Balance', value: obj.balance },
    ]);
  } else if (tablename === 'ship_special_weapon') {
    labels.push(...[
      { label: 'Damage', value: Number(obj.damage).toLocaleString() },
      { label: 'Range', value: `${obj.range}m` },
      { label: 'Critical', value: `${obj.critical}%` },
      { label: 'EN Usage', value: Number(obj.en_usage).toLocaleString() },
      { label: 'Reloadspeed', value: `${obj.reloadspeed}s` },
      { label: 'Hit range', value: `${obj.hitrange}m` },
      { label: 'Balance', value: obj.balance },
    ]);
  }

  return (
    <Card
      header={(
        <CardHeader>
          <CardHeaderTitle>Ship Attributes</CardHeaderTitle>
        </CardHeader>
        )}
    >
      <div className="divide-y divide-gray-200 dark:divide-dark-4">
        {labels.map((labelItem) => (
          <div key={labelItem.label} className="flex flex-col px-4 py-2">
            <div className="flex flex-row justify-between text-gray-700 dark:text-white">
              <span className="font-semibold">{labelItem.label}</span>
              <span>{labelItem.value}</span>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
};

export default ShipInformation;
