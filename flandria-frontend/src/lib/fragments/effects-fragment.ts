import {graphql} from "@/gql"
import {EffectFragmentFragment, EffectsFragmentFragment} from "@/gql/graphql"

export const EffectFragment = graphql(`
  fragment EffectFragment on Effect {
    effect_code
    operator
    value
  }
`)

export type Effect = EffectFragmentFragment

export const EffectsFragment = graphql(`
  fragment EffectsFragment on EffectMixin {
    effects {
      ...EffectFragment
    }
  }
`)

export type Effects = EffectsFragmentFragment
