import {gqlClient} from "@/lib/graphql-client"

import {graphql} from "@/gql"
import {BaseClassType} from "@/gql/graphql"

import {queryOptions} from "@tanstack/react-query"

const plannerQuery = graphql(`
  query PlannerData($codes: [String!]!) {
    all_player_skills(limit: -1, filter: {reference_code: {in: $codes}}) {
      skills: items {
        ...PlannerPlayerSkill
      }
    }
  }
`)

export const makePlannerQueryOptions = (
  baseClass: BaseClassType,
  referenceCodes: string[],
) =>
  queryOptions({
    queryKey: ["planner", baseClass, referenceCodes],
    queryFn: async () =>
      gqlClient.request(plannerQuery, {
        codes: referenceCodes,
      }),
  })
