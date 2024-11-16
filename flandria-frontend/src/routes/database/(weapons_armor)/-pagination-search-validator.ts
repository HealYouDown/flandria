import {pageValidator} from "@/utils/search-validators/page-validator"
import {searchStringValidator} from "@/utils/search-validators/search-string-validator"
import {sortDirectionValidatorWithDescDefault} from "@/utils/search-validators/sort-direction-validators"

import {
  CariadSort,
  CoatSort,
  DaggerSort,
  DualsSort,
  FishingRodSort,
  GauntletSort,
  OneHandedSwordSort,
  PantsSort,
  RapierSort,
  RifleSort,
  ShieldSort,
  ShoesSort,
  TwoHandedSwordSort,
} from "@/gql/graphql"

import {ComboboxOption} from "@/components/combobox"
import {characterClassValidators} from "@/components/filters/CharacterClassFilterSection"
import {effectsValidator} from "@/components/filters/EffectsFilterSection"
import {itemGradeValidator} from "@/components/filters/ItemGradeFilterSection"

import {fallback, zodSearchValidator} from "@tanstack/router-zod-adapter"
import {z} from "zod"

type Sorts =
  | CariadSort
  | RapierSort
  | DaggerSort
  | OneHandedSwordSort
  | TwoHandedSwordSort
  | ShieldSort
  | RifleSort
  | DualsSort
  | CoatSort
  | PantsSort
  | GauntletSort
  | ShoesSort
  | FishingRodSort
type AllowedSortOptions = keyof Sorts
export const sortOptions: ComboboxOption<AllowedSortOptions>[] = [
  {
    label: "Added",
    value: "row_id",
  },
  {
    label: "Name",
    value: "name",
  },
  {
    label: "Level Land",
    value: "level_land",
  },
  {
    label: "Level Sea",
    value: "level_sea",
  },
] as const
export const sortKeyValidator = z.custom<AllowedSortOptions>((val) =>
  sortOptions.map((o) => o.value).includes(val),
)

export const searchValidator = zodSearchValidator(
  z.object({
    page: pageValidator,
    s: searchStringValidator,
    sk: fallback(sortKeyValidator, "level_land").default("level_land"),
    sd: sortDirectionValidatorWithDescDefault,
    cc: fallback(characterClassValidators.nullable(), null).default(null),
    grade: fallback(itemGradeValidator.nullable(), null).default(null),
    effects: fallback(effectsValidator, []).default([]),
  }),
)
