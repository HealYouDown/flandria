import {TablenameLinkMapping} from "@/utils/format-helpers"

export function last<T>(array: T[]): T | undefined {
  return array[array.length - 1]
}

export function titleCase(str: string): string {
  return str.toLowerCase().replace(/\b\w/g, (s) => s.toUpperCase())
}

export function getLinkFromTablename(tablename: string) {
  const mapping: TablenameLinkMapping = {
    fishing_bait: "/database/fishing_bait/$code",
    duals: "/database/duals/$code",
    hat: "/database/hat/$code",
    pet_combine_help: "/database/pet_combine_help/$code",
    ship_normal_weapon: "/database/ship_normal_weapon/$code",
    upgrade_help: "/database/upgrade_help/$code",
    ship_flag: "/database/ship_flag/$code",
    random_box: "/database/random_box/$code",
    ship_front: "/database/ship_front/$code",
    pants: "/database/pants/$code",
    // fusion_help: "/database/fusion_help/$code",
    quest_item: "/database/quest_item/$code",
    pet_combine_stone: "/database/pet_combine_stone/$code",
    cariad: "/database/cariad/$code",
    two_handed_sword: "/database/two_handed_sword/$code",
    rapier: "/database/rapier/$code",
    pet_skill: "/database/pet_skill_stone/$code",
    shield: "/database/shield/$code",
    material: "/database/material/$code",
    quest_scroll: "/database/quest_scroll/$code",
    ship_shell: "/database/ship_shell/$code",
    seal_break_help: "/database/seal_break_help/$code",
    fishing_rod: "/database/fishing_rod/$code",
    ship_special_weapon: "/database/ship_special_weapon/$code",
    accessory: "/database/accessory/$code",
    ship_head_mast: "/database/ship_head_mast/$code",
    shoes: "/database/shoes/$code",
    skill_book: "/database/skill_book/$code",
    recipe: "/database/recipe/$code",
    essence: "/database/essence/$code",
    ship_magic_stone: "/database/ship_magic_stone/$code",
    ship_anchor: "/database/ship_anchor/$code",
    fishing_material: "/database/fishing_material/$code",
    bullet: "/database/bullet/$code",
    dagger: "/database/dagger/$code",
    rifle: "/database/rifle/$code",
    ship_body: "/database/ship_body/$code",
    pet_skill_stone: "/database/pet_skill_stone/$code",
    upgrade_crystal: "/database/upgrade_crystal/$code",
    essence_help: "/database/essence_help/$code",
    pet: "/database/pet/$code",
    one_handed_sword: "/database/one_handed_sword/$code",
    dress: "/database/dress/$code",
    production_book: "/database/production_book/$code",
    coat: "/database/coat/$code",
    ship_figure: "/database/ship_figure/$code",
    ship_main_mast: "/database/ship_main_mast/$code",
    consumable: "/database/consumable/$code",
    riding_pet: "/database/riding_pet/$code",
    upgrade_stone: "/database/upgrade_stone/$code",
    gauntlet: "/database/gauntlet/$code",
  }
  const value = mapping[tablename]
  if (value === undefined) throw new Error("unknown tablename " + tablename)
  return value
}
export function uniqueBy<T, K>({
  array,
  keyFn,
}: {
  array: T[]
  keyFn: (a: T) => K
}): T[] {
  const seen = new Set<K>()
  return array.filter((item) => {
    const key = keyFn(item)
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })
}

export function clamp(num: number, min: number, max: number): number {
  return Math.max(min, Math.min(num, max))
}
