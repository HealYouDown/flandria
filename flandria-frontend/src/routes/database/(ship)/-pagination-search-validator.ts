import {pageValidator} from "@/utils/search-validators/page-validator"
import {searchStringValidator} from "@/utils/search-validators/search-string-validator"
import {sortDirectionValidatorWithDescDefault} from "@/utils/search-validators/sort-direction-validators"

import {
  ShipAnchorSort,
  ShipBodySort,
  ShipFigureSort,
  ShipFrontSort,
  ShipHeadMastSort,
  ShipMagicStoneSort,
  ShipNormalWeaponSort,
  ShipSpecialWeaponSort,
} from "@/gql/graphql"

import {ComboboxOption} from "@/components/combobox"
import {effectsValidator} from "@/components/filters/EffectsFilterSection"
import {itemGradeValidator} from "@/components/filters/ItemGradeFilterSection"
import {shipClassValidator} from "@/components/filters/ShipClassFilterSection"

import {fallback, zodSearchValidator} from "@tanstack/router-zod-adapter"
import {z} from "zod"

type Sorts =
  | ShipBodySort
  | ShipFrontSort
  | ShipHeadMastSort
  | ShipFigureSort
  | ShipMagicStoneSort
  | ShipAnchorSort
  | ShipNormalWeaponSort
  | ShipSpecialWeaponSort
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
    sk: fallback(sortKeyValidator, "level_sea").default("level_sea"),
    sd: sortDirectionValidatorWithDescDefault,
    sc: fallback(shipClassValidator.nullable(), null).default(null),
    grade: fallback(itemGradeValidator.nullable(), null).default(null),
    effects: fallback(effectsValidator, []).default([]),
  }),
)
