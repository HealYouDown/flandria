import React from 'react';
import { armorTables, shipTables, weaponTables } from '../../../../constants';
import { resolveBoolToString, resolveLandClassNames, resolveSeaClassNames } from '../../../../helpers';
import Card, { CardHeader, CardHeaderTitle } from '../../../shared/Card';

function getBaseSubs(obj) {
  return [
    {
      label: 'Stack Size',
      value: obj.stack_size,
      description: 'The maximum stack size for an item.',
    },
    {
      label: 'Tradable',
      value: resolveBoolToString(obj.tradable),
      description: 'Whether an item can be traded with other players.',
    },
    {
      label: 'Destroyable',
      value: resolveBoolToString(obj.destroyable),
      description: 'Whether an item can be destroyed.',
    },
    {
      label: 'Sellable',
      value: resolveBoolToString(obj.sellable),
      description: 'Whether an item can be sold to NPCs.',
    },
    {
      label: 'Storagable',
      value: resolveBoolToString(obj.storagable),
      description: 'Whether an item can be stored in the private bank.',
    },
    {
      key: 'npc_buy_price',
      label: 'Buy Price',
      value: Number(obj.npc_buy_price).toLocaleString(),
      description: 'The price of the item if it can be bought at a NPC.',
    },
    {
      key: 'npc_sell_price',
      label: 'Sell Price',
      value: Number(obj.npc_sell_price).toLocaleString(),
      description: 'The price any NPC pays you for the item.',
    },
  ];
}

const InformationWidget = ({ tablename, obj, className }) => {
  const informationItems = [];

  if (tablename === 'guild') {
    informationItems.push(...[
      {
        label: 'Server',
        value: obj.server.name,
      },
      {
        label: 'Members',
        value: obj.member_count,
      },
      {
        label: 'Avg. Rank',
        value: Number(obj.avg_rank.toFixed(2)).toLocaleString(),
        description: 'Average rank (from the official ranking) of all members.',
      },
      {
        label: 'Avg. Level Land',
        value: Number(obj.avg_level_land.toFixed(2)).toLocaleString(),
        description: 'Average land level of all members.',
      },
      {
        label: 'Avg. Level Sea',
        value: Number(obj.avg_level_sea.toFixed(2)).toLocaleString(),
        description: 'Average sea level of all members.',
      },
    ]);
  } else if (tablename === 'player') {
    informationItems.push(...[
      {
        label: 'Server',
        value: obj.server.name,
      },
      {
        label: 'Class',
        value: obj.character_class.name,
      },
      {
        label: 'Guild',
        value: obj.guild ? obj.guild : '/',
      },
      {
        label: 'Level',
        value: `${obj.level_land} / ${obj.level_sea}`,
      },
      {
        label: 'Rank',
        value: Number(obj.rank).toLocaleString(),
        description: 'The rank from the official ranking.',
      },
      {
        label: 'Last Updated',
        value: obj.last_updated ? new Date(obj.last_updated).toLocaleDateString() : '/',
        description: 'When the user was last updated with data from the ranking.',
      },
      {
        label: 'Indexed At',
        value: new Date(obj.indexed_at).toLocaleDateString(),
        description: 'The date when the user was indexed from the ranking into the Flandria database.',
      },
    ]);
  } else if (tablename === 'monster') {
    informationItems.push(...[
      { label: 'Type', value: obj.rating.name },
      { label: 'Area', value: obj.area.name },
      { label: 'Level', value: obj.level },
      { label: 'HP', value: Number(obj.hp).toLocaleString() },
      { label: 'Physical Defense', value: Number(obj.physical_defense).toLocaleString() },
      { label: 'Magic Defense', value: Number(obj.magic_defense).toLocaleString() },
      { label: 'Damage', value: `${Number(obj.minimal_damage).toLocaleString()} ~ ${Number(obj.maximal_damage).toLocaleString()}` },
      { label: 'Range', value: `${obj.attack_range}m, ${obj.range.name}` },
      { label: 'Experience', value: Number(obj.experience).toLocaleString() },
      {
        label: 'Vision Range',
        value: `${obj.vision_range}m`,
        description: 'Aggression range when standing close to the monster.',
      },
      {
        label: 'Attack Vision Range',
        value: `${obj.attack_vision_range}m`,
        description: 'The aggression range when monsters nearby are attacked.',
      },
    ]);
  } else if (weaponTables.includes(tablename) || armorTables.includes(tablename) || tablename === 'fishing_rod') {
    if (tablename === 'shield') {
      informationItems.push(...[
        {
          label: 'Physical Defense',
          value: Number(obj.physical_defense).toLocaleString(),
        },
        {
          label: 'Magical Defense',
          value: Number(obj.magic_defense).toLocaleString(),
        },
      ]);
    }
    informationItems.push(...[
      {
        label: 'Class',
        value: resolveLandClassNames(obj.class_land),
      },
      {
        label: 'Level',
        value: `${obj.level_land}/${obj.level_sea}`,
      },
      ...getBaseSubs(obj),
    ]);
  } else if (['dress', 'hat', 'accessory'].includes(tablename)) {
    informationItems.push(...[
      {
        label: 'Class',
        value: resolveLandClassNames(obj.class_land),
      },
      {
        label: 'Gender',
        value: obj.gender.name,
      },
      {
        label: 'Level',
        value: `${obj.level_land}/${obj.level_sea}`,
      },
      ...getBaseSubs(obj),
    ]);
  } else if (['quest_scroll', 'essence_help', 'recipe', 'material', 'product_book', 'ship_flag', 'pet_skill_stone', 'riding_pet', 'seal_break_help', 'upgrade_help', 'upgrade_crystal', 'upgrade_stone', 'fishing_material', 'fishing_bait', 'random_box', 'skill_book', 'bullet'].includes(tablename)) {
    informationItems.push(...getBaseSubs(obj));
  } else if (tablename === 'quest_item') {
    informationItems.push(...getBaseSubs(
      obj,
    ).filter((sub) => !['npc_buy_price', 'npc_sell_price'].includes(sub.key)));
  } else if (tablename === 'essence') {
    informationItems.push(...[
      {
        label: 'Equip Type',
        value: obj.equip_type.name,
        description: 'Items the essence can be applied to.',
      },
      {
        label: 'Essence Type',
        value: obj.is_core_essence ? 'Core' : 'Meta',
        description: 'Whether the essence needs a core (golden) or meta (blue) slot.',
      },
      {
        label: 'Level',
        value: obj.required_weapon_level,
        description: 'The required weapon level to be able to apply the essence to.',
      },
      ...getBaseSubs(obj),
    ]);
  } else if (tablename === 'production') {
    informationItems.push(...[
      {
        label: 'Production Type',
        value: obj.production_type.name,
        description: 'The second job that can produce the item.',
      },
      {
        label: 'Points Needed',
        value: obj.points_needed,
        description: 'Amount of points to be able to learn the recipe.',
      },
    ]);
  } else if (shipTables.includes(tablename)) {
    informationItems.push(...[
      {
        label: 'Ship Class',
        value: resolveSeaClassNames(obj.class_sea),
      },
      {
        label: 'Level Sea',
        value: obj.level_sea,
      },
      ...getBaseSubs(obj),
      {
        label: 'Tuning Price',
        value: Number(obj.npc_tuning_price).toLocaleString(),
        description: 'Price to tune your ship with this item at the Dock Manager.',
      },
    ]);
  } else if (tablename === 'ship_shell') {
    informationItems.push(...[
      {
        label: 'Level',
        value: obj.level,
      },
      {
        label: 'Damage',
        value: obj.damage,
      },
      {
        label: 'Explosion Range',
        value: `${obj.explosion_range}m`,
      },
      ...getBaseSubs(obj),
    ]);
  } else if (tablename === 'pet_combine_help') {
    informationItems.push(...[
      {
        label: 'Efficiency',
        value: `${obj.efficiency}%`,
      },
      ...getBaseSubs(obj),
    ]);
  } else if (tablename === 'pet_combine_stone') {
    informationItems.push(...[
      {
        label: 'Efficiency',
        value: `${obj.efficiency_minimal} ~ ${obj.efficiency_maximal}`,
        description: 'Possible increment when using this stone. Maximum for each stat is 10.000.',
      },
      ...getBaseSubs(obj),
    ]);
  } else if (tablename === 'pet') {
    informationItems.push(...[
      {
        label: 'Pocketwatches',
        value: resolveBoolToString(!obj.is_unlimited),
        description: 'Whether a Pet needs pocket watches to be able to be summoned.',
      },
      ...getBaseSubs(obj),
    ]);
  } else if (tablename === 'consumable') {
    informationItems.push(...[
      {
        label: 'Level',
        value: `${obj.level_land}/${obj.level_sea}`,
      },
      {
        label: 'Cooldown',
        value: `${obj.cooldown}s`,
      },
      {
        label: 'Cast Time',
        value: `${obj.cast_time}`,
      },
      {
        label: 'Efficiency',
        value: Number(obj.efficiency).toLocaleString(),
      },
      ...getBaseSubs(obj),
    ]);
  } else if (tablename === 'npc') {
    informationItems.push(...[
      {
        label: 'Level',
        value: `${obj.level}`,
      },
    ]);
  } else if (tablename === 'quest') {
    informationItems.push(...[
      {
        label: 'Class',
        value: resolveLandClassNames(obj.class),
      },
      {
        label: 'Level',
        value: obj.level,
      },
      {
        label: 'Area',
        value: obj.area.name,
      },
      {
        label: 'Start Map',
        value: obj.start_area ? obj.start_area.name : '/',
        description: 'The map where the quest starts.',
      },
      {
        label: 'Start NPC',
        value: obj.start_npc ? obj.start_npc.name : '/',
        description: 'The NPC that gives you the quest.',
      },
      {
        label: 'End NPC',
        value: obj.end_npc ? obj.end_npc.name : '/',
        description: 'The NPC you have to talk to to finish the quest.',
      },
      {
        label: 'Money',
        value: Number(obj.money).toLocaleString(),
        description: 'The reward money once you finish the quest.',
      },
      {
        label: 'Experience',
        value: Number(obj.experience).toLocaleString(),
        description: 'The reward experience once you finish the quest.',
      },
    ]);
  }

  return (
    <Card
      className={className}
      header={(
        <CardHeader>
          <CardHeaderTitle>Attributes</CardHeaderTitle>
        </CardHeader>
      )}
    >
      <div className="divide-y divide-gray-200 dark:divide-dark-4">
        {informationItems.map((informationItem) => (
          <div key={informationItem.label} className="flex flex-col px-4 py-2">
            <div className="flex flex-row justify-between text-gray-700 dark:text-white">
              <span className="font-semibold">{informationItem.label}</span>
              <span>{informationItem.value}</span>
            </div>
            {informationItem.description && (
            <small className="text-xs leading-none text-gray-400 dark:text-white dark:text-opacity-70">
              {informationItem.description}
            </small>
            )}
          </div>
        ))}
      </div>
    </Card>
  );
};

export default InformationWidget;
