import {graphql} from "@/gql"

export const weaponPaginationFragment = graphql(`
  fragment WeaponPaginationFragment on WeaponMixin {
    code
    name
    icon
    grade
    level_land
    level_sea
    duration
    ...CharacterClassFragment
    effects {
      effect_code
      operator
      value
    }
  }
`)

export const armorPaginationFragment = graphql(`
  fragment ArmorPaginationFragment on ArmorMixin {
    code
    name
    icon
    grade
    level_land
    level_sea
    duration
    ...CharacterClassFragment
    effects {
      effect_code
      operator
      value
    }
  }
`)
