import {graphql} from "@/gql"

export const CharacterClassFragment = graphql(`
  fragment CharacterClassFragment on ClassLandMixin {
    is_noble
    is_magic_knight
    is_court_magician

    is_mercenary
    is_gladiator
    is_guardian_swordsman

    is_explorer
    is_excavator
    is_sniper

    is_saint
    is_priest
    is_shaman
  }
`)
