import {Combobox, ComboboxOption} from "@/components/combobox"
import {FilterMenuChildrenRenderProps} from "@/components/pagination-filter"

import {UseNavigateResult} from "@tanstack/react-router"
import {z} from "zod"

type ActorTypeOptions = "land" | "sea"
const areaFilterOptions: ComboboxOption<ActorTypeOptions>[] = [
  {
    label: "Land",
    value: "land",
  },
  {
    label: "Sea",
    value: "sea",
  },
] as const

export const landSeaValidator = z.custom<ActorTypeOptions>((val) =>
  areaFilterOptions.map((o) => o.value).includes(val),
)

type LandSeaFilterSectionProps = {
  area: ActorTypeOptions | null
  navigate: UseNavigateResult<"/">
} & FilterMenuChildrenRenderProps

export function LandSeaFilterSection({
  Section,
  Label,
  area,
  navigate,
}: LandSeaFilterSectionProps) {
  return (
    <Section>
      <Label htmlFor="land-sea-filter">Area</Label>
      <Combobox
        nullable
        id="land-sea-filter"
        triggerClassName="col-span-2"
        value={area}
        options={areaFilterOptions}
        onValueChange={(value) => {
          navigate({
            search: (prev) => ({
              ...prev,
              page: 1,
              area: value,
            }),
          })
        }}
      />
    </Section>
  )
}
