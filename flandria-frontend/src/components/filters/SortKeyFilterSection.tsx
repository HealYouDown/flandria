import {Combobox, ComboboxOption} from "@/components/combobox"
import {FilterMenuChildrenRenderProps} from "@/components/pagination-filter"

import {UseNavigateResult} from "@tanstack/react-router"

type SortKeyFilterSectionProps<T> = {
  sortKey: T
  sortOptions: ComboboxOption<T>[]
  navigate: UseNavigateResult<"/">
} & FilterMenuChildrenRenderProps

export function SortKeyFilterSection<T>({
  Section,
  Label,
  sortKey,
  sortOptions,
  navigate,
}: SortKeyFilterSectionProps<T>) {
  return (
    <Section>
      <Label htmlFor="sort-key">Sort</Label>
      <Combobox
        nullable={false}
        id="sort-key"
        triggerClassName="col-span-2"
        value={sortKey}
        options={sortOptions}
        onValueChange={(value) => {
          navigate({
            search: (prev) => ({
              ...prev,
              sk: value,
            }),
          })
        }}
      />
    </Section>
  )
}
