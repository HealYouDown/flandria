const classLandFilter = {
  "Noble": "class_land:Noble",
  "Magic Knight": "class_land:Magic Knight",
  "Court Magican": "class_land:Court Magican",
  "Mercenary": "class_land:Mercenary",
  "Gladiator": "class_land:Gladiator",
  "Guardian Swordman": "class_land:Guardian Swordman",
  "Saint": "class_land:Saint",
  "Priest": "class_land:Priest",
  "Shaman": "class_land:Shaman",
  "Explorer": "class_land:Explorer",
  "Excavator": "class_land:Excavator",
  "Sniper": "class_land:Sniper",
}

const weaponAndArmorFilter = {
  "sort": {
    "Land Level": "level_land",
    "Sea Level": "level_sea",
  },
  "filter": classLandFilter,
}

const tableToFilters = {
  "monster": {
    "location": true,
    "sort": {
      "Level": "level",
      "HP": "hp",
      "Experience": "experience",
      "Min. Dmg": "min_dmg",
      "Max. Dmg": "max_dmg",
    },
    "filter": {
      "Normal Monster": "monster_rating:0",
      "Elite Monster": "monster_rating:1",
      "Boss": "monster_rating:2",
      "Island Boss": "monster_rating:3",
    },
  },
  "hat": {
    "bonus": true,
  },
  "dress": {
    "bonus": true
  },
  "cariad": weaponAndArmorFilter,
  "rapier": weaponAndArmorFilter,
  "dagger": weaponAndArmorFilter,
  "one_handed_sword": weaponAndArmorFilter,
  "two_handed_sword": weaponAndArmorFilter,
  "shield": weaponAndArmorFilter,
  "rifle": weaponAndArmorFilter,
  "duals": weaponAndArmorFilter,
  "coat": weaponAndArmorFilter,
  "pants": weaponAndArmorFilter,
  "gauntlet": weaponAndArmorFilter,
  "shoes": weaponAndArmorFilter,
  "quest": {
    "location": true,
    "sort": {
      "Level": "level",
    },
  },
  "accessory": {
    "sort": {
      "Level": "level_land",
    },
  },
}

export {
  tableToFilters,
}