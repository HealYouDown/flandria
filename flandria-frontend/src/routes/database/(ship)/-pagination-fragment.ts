import {graphql} from "@/gql"

export const shipPaginationFragment = graphql(`
  fragment ShipPaginationFragment on ShipBaseMixin {
    code
    name
    icon
    grade
    level_sea
    duration
    ...ShipClassFragment
    effects {
      effect_code
      operator
      value
    }
  }
`)
