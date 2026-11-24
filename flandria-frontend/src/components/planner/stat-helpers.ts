import {BaseClassType} from "@/lib/enums"

import {CharacterStats} from "@/components/planner/stat-formulas.generated"

export type InvestedStats = {
  strength: number
  dexterity: number
  constitution: number
  intelligence: number
  wisdom: number
  will: number
}

export const NO_INVESTED_STATS: InvestedStats = {
  strength: 0,
  dexterity: 0,
  constitution: 0,
  intelligence: 0,
  wisdom: 0,
  will: 0,
}

export const MAX_INVEST_POINTS = 500

// Sea levels above this don't grant stat points anymore
export const SEA_LEVEL_STAT_POINT_CAP = 69

export const BASE_STATS: Record<
  Exclude<BaseClassType, BaseClassType.Ship>,
  InvestedStats
> = {
  [BaseClassType.Explorer]: {
    strength: 19,
    dexterity: 18,
    constitution: 16,
    intelligence: 13,
    wisdom: 10,
    will: 17,
  },
  [BaseClassType.Noble]: {
    strength: 11,
    dexterity: 16,
    constitution: 12,
    intelligence: 21,
    wisdom: 19,
    will: 14,
  },
  [BaseClassType.Saint]: {
    strength: 14,
    dexterity: 14,
    constitution: 14,
    intelligence: 16,
    wisdom: 19,
    will: 16,
  },
  [BaseClassType.Mercenary]: {
    strength: 21,
    dexterity: 15,
    constitution: 22,
    intelligence: 8,
    wisdom: 10,
    will: 17,
  },
}

// 3 at creation + 3 per land level, 1 per sea level (capped)
export function availableStatPoints(levelLand: number, levelSea: number) {
  return 3 * levelLand + Math.min(levelSea, SEA_LEVEL_STAT_POINT_CAP) - 1
}

export function toCharacterStats(stats: InvestedStats): CharacterStats {
  return {
    str: stats.strength,
    dex: stats.dexterity,
    con: stats.constitution,
    int: stats.intelligence,
    wis: stats.wisdom,
    vol: stats.will,
  }
}
