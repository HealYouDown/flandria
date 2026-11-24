import {clamp} from "@/utils/utils"

import {graphql} from "@/gql"
import {PlannerPlayerSkillFragment} from "@/gql/graphql"

export const SKILL_PLANNER_WIDTH = 448
export const SKILL_PLANNER_HEIGHT = 503

// Level from which the second class can be selected
export const CLASS_MIN_LEVEL = 40

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

export type SkillLevels<TCode extends string> = {[key in TCode]: number}
export type LevelSkillData = {[level: number]: PlayerSkill}
export type GroupedSkillData<TCode extends string> = {
  [key in TCode]: LevelSkillData
}

export type SkillBuild<TCode extends string> = {
  level: number
  class: ClassFlagsType | null
  skills: SkillLevels<TCode>
}

export type SkillTree<TCode extends string> = {
  skills: GroupedSkillData<TCode>
  // Classes that can always be skilled (the base class, or all ship classes)
  alwaysAllowedClasses: ClassFlagsType[]
  // Selectable second classes, null if there are none (ship)
  classOptions: ClassFlagsType[] | null
  maxLevel: number
}

export function makeSkillLevels<TCode extends string>(
  codes: TCode[],
  level: number = 0,
): SkillLevels<TCode> {
  return Object.fromEntries(
    codes.map((code) => [code, level]),
  ) as SkillLevels<TCode>
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

export function getAvailableSkillPoints(level: number): number {
  return level
}

function requiredLevel(skill: PlayerSkill): number {
  return skill.required_level_land === 0
    ? skill.required_level_sea
    : skill.required_level_land
}

// Highest skill level that can be reached at the given character level
export function maxReachableSkillLevel(
  skillData: LevelSkillData,
  level: number,
): number {
  return Math.max(
    0,
    ...Object.values(skillData)
      .filter((skill) => requiredLevel(skill) <= level)
      .map((skill) => skill.skill_level),
  )
}

export function isClassAllowed(
  skill: PlayerSkill,
  allowedClasses: ClassFlagsType[],
): boolean {
  const requiredClasses = CLASS_FLAGS.filter((flag) => skill[flag])
  // Some skills (looking at you sea) don't require any class
  return (
    requiredClasses.length === 0 ||
    requiredClasses.some((flag) => allowedClasses.includes(flag))
  )
}

export function getAllowedClasses<TCode extends string>(
  tree: SkillTree<TCode>,
  selectedClass: ClassFlagsType | null,
): ClassFlagsType[] {
  return selectedClass === null
    ? tree.alwaysAllowedClasses
    : [...tree.alwaysAllowedClasses, selectedClass]
}

// Brings a (possibly loaded or changed) build into a valid state: the class is
// only kept if selectable at that level, every skill is capped to what the
// level allows, and skills whose class is not allowed or whose required skills
// are not learned are reset, which cascades through the whole tree.
export function normalizeSkillBuild<TCode extends string>(
  build: SkillBuild<TCode>,
  tree: SkillTree<TCode>,
): SkillBuild<TCode> {
  const level = clamp(Math.trunc(build.level) || 1, 1, tree.maxLevel)
  const selectedClass =
    level >= CLASS_MIN_LEVEL &&
    build.class !== null &&
    tree.classOptions?.includes(build.class)
      ? build.class
      : null
  const allowedClasses = getAllowedClasses(tree, selectedClass)

  const skills = {} as SkillLevels<TCode>
  const resolve = (code: TCode): number => {
    if (code in skills) return skills[code]
    skills[code] = 0 // guards against cycles

    const skillData = tree.skills[code]
    if (!skillData) return 0

    const baseSkill = skillData[0]
    const requirementsMet = baseSkill.required_skills.every(
      (s) => resolve(s.required_skill_code as TCode) >= 1,
    )
    if (requirementsMet && isClassAllowed(baseSkill, allowedClasses)) {
      const wanted = Math.trunc(build.skills[code] ?? 0) || 0
      skills[code] = clamp(wanted, 0, maxReachableSkillLevel(skillData, level))
    }
    return skills[code]
  }
  ;(Object.keys(tree.skills) as TCode[]).forEach(resolve)

  return {level, class: selectedClass, skills}
}

export function canLevelUpSkill<TCode extends string>(
  build: SkillBuild<TCode>,
  tree: SkillTree<TCode>,
  code: TCode,
): boolean {
  const skillData = tree.skills[code]
  const baseSkill = skillData[0]
  return (
    isClassAllowed(baseSkill, getAllowedClasses(tree, build.class)) &&
    baseSkill.required_skills.every(
      (s) => (build.skills[s.required_skill_code as TCode] ?? 0) >= 1,
    ) &&
    build.skills[code] < maxReachableSkillLevel(skillData, build.level)
  )
}

export function usedSkillPoints<TCode extends string>(
  skills: SkillLevels<TCode>,
): number {
  return (Object.values(skills) as number[]).reduce((a, b) => a + b, 0)
}

// Sets a skill level, an increase is capped by the remaining skill points
export function setSkillLevel<TCode extends string>(
  build: SkillBuild<TCode>,
  tree: SkillTree<TCode>,
  code: TCode,
  newLevel: number,
): SkillBuild<TCode> {
  const currentLevel = build.skills[code]
  if (newLevel > currentLevel) {
    const remaining =
      getAvailableSkillPoints(build.level) - usedSkillPoints(build.skills)
    newLevel = Math.min(newLevel, currentLevel + Math.max(remaining, 0))
  }
  return normalizeSkillBuild(
    {...build, skills: {...build.skills, [code]: newLevel}},
    tree,
  )
}
