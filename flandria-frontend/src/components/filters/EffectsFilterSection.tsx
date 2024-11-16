import {effectCodeMapping} from "@/utils/format-helpers"

import {EffectCode} from "@/gql/graphql"

import {ComboboxOption} from "@/components/combobox"
import {MultiCombobox} from "@/components/multi-combobox"
import {FilterMenuChildrenRenderProps} from "@/components/pagination-filter"

import {UseNavigateResult} from "@tanstack/react-router"
import {z} from "zod"

const effectsFilterOptions: ComboboxOption<EffectCode>[] = Object.keys(
  effectCodeMapping,
).map((key) => ({
  label: effectCodeMapping[key as EffectCode]!,
  value: key as EffectCode,
}))

export const effectsValidator = z
  .custom<EffectCode>((val) =>
    effectsFilterOptions.map((o) => o.value).includes(val),
  )
  .array()

type EffectsFilterSectionProps = {
  effects: EffectCode[]
  navigate: UseNavigateResult<"/">
} & FilterMenuChildrenRenderProps

export function EffectsFilterSection({
  Section,
  Label,
  effects,
  navigate,
}: EffectsFilterSectionProps) {
  return (
    <Section>
      <Label htmlFor="effects">Effects</Label>
      <MultiCombobox
        id="effects"
        triggerClassName="col-span-2"
        value={effects}
        options={effectsFilterOptions}
        onValueChange={(value) => {
          navigate({
            search: (prev) => ({
              ...prev,
              page: 1,
              effects: value,
            }),
          })
        }}
      />
    </Section>
  )
}
