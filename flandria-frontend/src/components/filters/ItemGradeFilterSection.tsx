import {ItemGrade} from "@/gql/graphql"

import {Combobox, ComboboxOption} from "@/components/combobox"
import {FilterMenuChildrenRenderProps} from "@/components/pagination-filter"

import {UseNavigateResult} from "@tanstack/react-router"
import {z} from "zod"

const itemGradeOptions: ComboboxOption<ItemGrade>[] = [
  {
    label: "Common",
    value: ItemGrade.Blue,
  },
  {
    label: "Rare",
    value: ItemGrade.Green,
  },
  {
    label: "Legendary",
    value: ItemGrade.Yellow,
  },
  {
    label: "Mythical",
    value: ItemGrade.Orange,
  },
] as const

export const itemGradeValidator = z.custom<ItemGrade>((val) =>
  itemGradeOptions.map((o) => o.value).includes(val),
)

type ItemGradeFilterSectionProps = {
  grade: ItemGrade | null
  navigate: UseNavigateResult<"/">
} & FilterMenuChildrenRenderProps

export function ItemGradeFilterSection({
  Section,
  Label,
  grade,
  navigate,
}: ItemGradeFilterSectionProps) {
  return (
    <Section>
      <Label htmlFor="item-grade">Rarity</Label>
      <Combobox
        nullable
        id="item-grade"
        triggerClassName="col-span-2"
        value={grade}
        options={itemGradeOptions}
        onValueChange={(value) => {
          navigate({
            search: (prev) => ({
              ...prev,
              page: 1,
              grade: value,
            }),
          })
        }}
      />
    </Section>
  )
}
