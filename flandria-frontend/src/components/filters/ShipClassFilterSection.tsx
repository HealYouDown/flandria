import {ObjThatSupportsShipClass} from "@/utils/format-helpers"

import {Combobox, ComboboxOption} from "@/components/combobox"
import {FilterMenuChildrenRenderProps} from "@/components/pagination-filter"

import {UseNavigateResult} from "@tanstack/react-router"
import {z} from "zod"

type ShipClassKeys = keyof ObjThatSupportsShipClass
const shipClassFilterOptions: ComboboxOption<ShipClassKeys>[] = [
  {
    label: "Big Gun",
    value: "is_big_gun",
  },
  {
    label: "Armored",
    value: "is_armored",
  },
  {
    label: "Torpedo",
    value: "is_torpedo",
  },
  {
    label: "Maintenance",
    value: "is_maintenance",
  },
  {
    label: "Assault",
    value: "is_assault",
  },
] as const

export const shipClassValidator = z.custom<ShipClassKeys>((val) =>
  shipClassFilterOptions.map((o) => o.value).includes(val),
)

type ShipClassFilterSectionProps = {
  cc: ShipClassKeys | null
  navigate: UseNavigateResult<"/">
} & FilterMenuChildrenRenderProps

export function ShipClassFilterSection({
  Section,
  Label,
  cc,
  navigate,
}: ShipClassFilterSectionProps) {
  return (
    <Section>
      <Label htmlFor="ship-class">Ship</Label>
      <Combobox
        nullable
        id="ship-class"
        triggerClassName="col-span-2"
        value={cc}
        options={shipClassFilterOptions}
        onValueChange={(value) => {
          navigate({
            search: (prev) => ({
              ...prev,
              page: 1,
              sc: value,
            }),
          })
        }}
      />
    </Section>
  )
}
