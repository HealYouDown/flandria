import {graphql} from "@/gql"

export const shipClassFragment = graphql(`
  fragment ShipClassFragment on ClassSeaMixin {
    is_armored
    is_big_gun
    is_assault
    is_torpedo
    is_maintenance
  }
`)
