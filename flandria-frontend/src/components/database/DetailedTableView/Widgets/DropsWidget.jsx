import React from 'react';
import ListWidget, { ItemListWidgetItem, TextListWidgetItem } from './ListWidget';

const tableValue = {
  essence: 11000,
  essence_help_item: 10500,

  material: 10000,

  upgrade_help: 9950,
  seal_break_help: 9949,

  pet_skill_stone: 9900,

  random_box: 9800,

  cariad: 1000,
  rapier: 999,
  dagger: 998,
  one_handed_sword: 997,
  two_handed_sword: 996,
  rifle: 995,
  duals: 994,
  shield: 993,

  hat: 800,
  dress: 799,
  accessory: 798,

  coat: 550,
  pants: 549,
  shoes: 548,
  gauntlet: 547,

  consumable: 300,

  upgrade_stone: 250,

  pet_combine_help: 200,
  pet_combine_stone: 199,

  ship_normal_weapon: 152,
  ship_special_weapon: 151,
  ship_body: 150,
  ship_front: 149,
  ship_head_mast: 148,
  ship_main_mast: 147,
  ship_figure: 146,
  ship_magic_stone: 145,
  ship_anchor: 144,
  ship_flag: 143,

  recipe: 100,
  quest_scroll: 99,
  quest_item: 98,

  bullet: 2,
  ship_shell: 1,
};

function sortDrops(a, b) {
  const tableValueA = tableValue[a.item.table];
  const tableValueB = tableValue[b.item.table];

  // First sort by table value
  if (tableValueA > tableValueB) return -1;
  if (tableValueA < tableValueB) return 1;

  // If they are the same, sort by name
  if (a.item.name > b.item.name) return 1;
  if (a.item.name < b.item.name) return -1;

  return 1;
}

const DropsWidget = ({ drops }) => (
  <ListWidget
    label="Drops"
  >
    {drops.sort(sortDrops).map((drop) => (
      <ItemListWidgetItem
        key={drop.id}
        tablename={drop.item.table}
        item={drop.item}
        subs={[`Qty. ${drop.quantity}x`]}
      />
    ))}
    {(drops.length === 0) && (
      <TextListWidgetItem><span>No drops found.</span></TextListWidgetItem>
    )}
  </ListWidget>
);

export default DropsWidget;
