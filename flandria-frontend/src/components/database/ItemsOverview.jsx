import React from 'react';
import { setWindowTitle } from '../../helpers';
import Card, { ClickableCardItem, CardHeader, CardHeaderTitle } from '../shared/Card';
import Grid, { Column } from '../shared/Grid';

const URLS = [
  [
    // Column 1
    {
      name: '⚔️ Weapons',
      subtext: 'Looking for some great weapons to improve your character? This section got you covered!',
      urls: [
        ['Cariads', '/database/cariad'],
        ['Rapiers', '/database/rapier'],
        ['Daggers', '/database/dagger'],
        ['One-handed Swords', '/database/one_handed_sword'],
        ['Two-handed Swords', '/database/two_handed_sword'],
        ['Shields', '/database/shield'],
        ['Rifles', '/database/rifle'],
        ['Duals', '/database/duals'],
      ],
    },
    {
      name: '🛡️ Armor',
      subtext: 'You want to be the best tank there ever was? Have a look at all the different armor and find something that fits your needs!',
      urls: [
        ['Coats', '/database/coat'],
        ['Pants', '/database/pants'],
        ['Gauntlets', '/database/gauntlet'],
        ['Shoes', '/database/shoes'],
      ],
    },
    {
      name: '💎 Extra Equipment',
      subtext: "Don't like the look of the default armor? Get a dress that makes you look fabulous!",
      urls: [
        ['Hats', '/database/hat'],
        ['Dresses', '/database/dress'],
        ['Accessories', '/database/accessory'],
      ],
    },
    {
      name: '🏹 Quests',
      subtext: 'Hunting Monsters and getting paid for it… what a dream!',
      urls: [
        ['Quest Scrolls', '/database/quest_scroll'],
        ['Quest Items', '/database/quest_item'],
      ],
    },
  ],
  [
    // Column 2
    {
      name: '⚖️ Essence',
      subtext: 'Essences allow your character to grow stronger in a unique way. Look through all options and select the ones you like!',
      urls: [
        ['Essences', '/database/essence'],
        ['Essence Help', '/database/essence_help'],
        ['Essence Recipes', '/database/production?filter=production:4'],
      ],
    },
    {
      name: '📜 Crafting',
      subtext: 'Standard items are lame? How about some shiny crafted ones?',
      urls: [
        ['Recipes', '/database/recipe'],
        ['Materials', '/database/material'],
        ['Second Job', '/database/production'],
        ['Second Job Books', '/database/product_book'],
      ],
    },
    {
      name: '⚓ Ship',
      subtext: 'Being a pirate on sea is way more fun, isn\'t it? You definitely need a big ship for that!',
      urls: [
        ['Bodies', '/database/ship_body'],
        ['Fronts', '/database/ship_front'],
        ['Head Masts', '/database/ship_head_mast'],
        ['Main Masts', '/database/ship_main_mast'],
        ['Figures', '/database/ship_figure'],
        ['Magic Stones', '/database/ship_magic_stone'],
        ['Anchors', '/database/ship_anchor'],
        ['Shell', '/database/ship_shell'],
        ['Flags', '/database/ship_flag'],
        ['Normal Weapon', '/database/ship_normal_weapon'],
        ['Special Weapon', '/database/ship_special_weapon'],
      ],
    },
  ],
  [
    // Column 3
    {
      name: '🐾 Pets',
      subtext: 'Looking for a little friend and helper always by your side?',
      urls: [
        ['Combine Help Item', '/database/pet_combine_help'],
        ['Combine Stone Item', '/database/pet_combine_stone'],
        ['Pet Skills', '/database/pet_skill_stone'],
        ['Pets', '/database/pet'],
        ['Riding Pets', '/database/riding_pet'],
      ],
    },
    {
      name: '🔮 Enhancing',
      subtext: 'You want to unseal the mighty power of your equipment? Enhancing offers you a lot of different options!',
      urls: [
        ['Seal Break Item', '/database/seal_break_help'],
        ['Upgrade Help Item', '/database/upgrade_help'],
        ['Upgrade Crystals', '/database/upgrade_crystal'],
        ['Upgrade Stone', '/database/upgrade_stone'],
      ],
    },
    {
      name: '🎣 Fishing',
      subtext: 'Sometimes fishing is relaxing. But just what fishing rod should be used?',
      urls: [
        ['Fishing Rods', '/database/fishing_rod'],
        ['Fishing Items', '/database/fishing_material'],
        ['Fishing Baits', '/database/fishing_bait'],
      ],
    },
    {
      name: '🔗 Others',
      subtext: 'Didn\'t find what you\'re looking for? Try one of the sections below!',
      urls: [
        ['Random Boxes', '/database/random_box'],
        ['Consumables', '/database/consumable'],
        ['Skill Books', '/database/skill_book'],
        ['Bullets', '/database/bullet'],
      ],
    },
  ],
];

const ItemsOverview = () => {
  setWindowTitle('Items Overview');

  return (
    <Grid gap="gap-6 gap-x-8">
      {URLS.map((column) => (
        <Column key={Math.random().toString()} gap="gap-6" md={4}>
          {column.map((section) => (
            <Card
              key={section.name}
              header={(
                <CardHeader>
                  <CardHeaderTitle>{section.name}</CardHeaderTitle>
                  <p className="text-sm leading-none text-gray-400 dark:text-white dark:text-opacity-70">
                    {section.subtext}
                  </p>
                </CardHeader>
            )}
            >
              <div className="divide-y divide-gray-200 dark:divide-dark-4">
                {section.urls.map((url) => (
                  <ClickableCardItem
                    key={url[1]}
                    to={url[1]}
                  >
                    {url[0]}
                  </ClickableCardItem>
                ))}
              </div>
            </Card>
          ))}
        </Column>
      ))}
    </Grid>
  );
};

export default ItemsOverview;
