const CLASSNAME_TO_INITIAL_POINTS = {
  explorer: {
    strength: 19,
    dexterity: 18,
    constitution: 16,
    intelligence: 13,
    wisdom: 10,
    will: 17,
  },
  noble: {
    strength: 11,
    dexterity: 16,
    constitution: 12,
    intelligence: 21,
    wisdom: 19,
    will: 14,
  },
  saint: {
    strength: 14,
    dexterity: 14,
    constitution: 14,
    intelligence: 16,
    wisdom: 19,
    will: 16,
  },
  mercenary: {
    strength: 21,
    dexterity: 15,
    constitution: 22,
    intelligence: 8,
    wisdom: 10,
    will: 17,
  },
};

const MAX_LEVEL_LAND = 105;
const MAX_LEVEL_SEA = 99;
const MAX_POINTS_LIMIT = 600;
const SHIFT_STATUS_INCREMENT = 15;

export {
  CLASSNAME_TO_INITIAL_POINTS, MAX_LEVEL_LAND, MAX_LEVEL_SEA, MAX_POINTS_LIMIT,
  SHIFT_STATUS_INCREMENT,
};
