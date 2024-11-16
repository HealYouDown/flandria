import {clamp} from "@/utils/utils"

import {graphql} from "@/gql"
import {PlannerPlayerSkillFragment} from "@/gql/graphql"

import {
  GroupedSkillData,
  SkillLevels,
} from "@/components/planner/skill-planner-card"

export const SKILL_PLANNER_WIDTH = 448
export const SKILL_PLANNER_HEIGHT = 503

graphql(`
  fragment PlannerPlayerSkillClassFlags on PlayerSkill {
    is_explorer
    is_sniper
    is_excavator

    is_noble
    is_court_magician
    is_magic_knight

    is_saint
    is_shaman
    is_priest

    is_mercenary
    is_gladiator
    is_guardian_swordsman

    is_torpedo
    is_armored
    is_assault
    is_big_gun
    is_maintenance
  }
`)

export const CLASS_FLAGS = [
  "is_explorer",
  "is_sniper",
  "is_excavator",

  "is_noble",
  "is_court_magician",
  "is_magic_knight",

  "is_saint",
  "is_shaman",
  "is_priest",

  "is_mercenary",
  "is_gladiator",
  "is_guardian_swordsman",

  "is_torpedo",
  "is_armored",
  "is_assault",
  "is_big_gun",
  "is_maintenance",
] as const
export type ClassFlagsType = (typeof CLASS_FLAGS)[number]

graphql(`
  fragment PlannerPlayerSkill on PlayerSkill {
    code
    reference_code
    icon
    name
    skill_level
    skill_max_level
    required_level_land
    required_level_sea
    mana_cost
    cast_distance
    cast_time
    effect_range
    cooldown
    description
    required_weapons
    ...PlannerPlayerSkillClassFlags

    required_skills {
      required_skill_code
    }
  }
`)
export type PlayerSkill = PlannerPlayerSkillFragment

export function makeSkillLevels<TCode extends string>(
  codes: TCode[],
  level: number = 0,
): SkillLevels<TCode> {
  return codes.reduce((acc, current) => {
    acc[current as TCode] = level
    return acc
  }, {} as SkillLevels<TCode>)
}

export function groupSkillsData<TCode extends string>(
  skills: PlayerSkill[],
): GroupedSkillData<TCode> {
  return skills.reduce((acc, current) => {
    const key = current.reference_code as TCode
    if (!(key in acc)) {
      acc[key] = {}
    }
    acc[key][current.skill_level] = current
    return acc
  }, {} as GroupedSkillData<TCode>)
}
export function getAvailableSkillPointsLand(level: number): number {
  if (level === 105) return 101
  return clamp(level, 1, 100)
}

export function getAvailableSkillPointsSea(level: number): number {
  return level
}
