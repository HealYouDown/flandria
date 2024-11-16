import {SortDirection} from "@/gql/graphql"

import {Combobox} from "@/components/combobox"
import {FilterMenuChildrenRenderProps} from "@/components/pagination-filter"

import {UseNavigateResult} from "@tanstack/react-router"

type SortDirectionFilterSectionProps = {
  direction: SortDirection
  navigate: UseNavigateResult<"/">
} & FilterMenuChildrenRenderProps

const sortDirectionFilterOptions = [
  {label: "Ascending", value: SortDirection.Asc},
  {label: "Descending", value: SortDirection.Desc},
]

export function SortDirectionFilterSection({
  Section,
  Label,
  direction,
  navigate,
}: SortDirectionFilterSectionProps) {
  return (
    <Section>
      <Label htmlFor="sort-direction">Order</Label>
      <Combobox
        nullable={false}
        id="sort-direction"
        triggerClassName="col-span-2"
        value={direction}
        options={sortDirectionFilterOptions}
        onValueChange={(value) => {
          navigate({
            search: (prev) => ({
              ...prev,
              sd: value,
            }),
          })
        }}
      />
    </Section>
  )
}
