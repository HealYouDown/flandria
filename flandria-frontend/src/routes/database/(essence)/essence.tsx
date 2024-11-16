import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {essenceEquipTypeToString} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {pageValidator} from "@/utils/search-validators/page-validator"
import {searchStringValidator} from "@/utils/search-validators/search-string-validator"
import {sortDirectionValidatorWithDescDefault} from "@/utils/search-validators/sort-direction-validators"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {EssenceEquipType, EssenceFilter, EssenceSort} from "@/gql/graphql"

import {Combobox, ComboboxOption} from "@/components/combobox"
import {
  EffectsFilterSection,
  effectsValidator,
} from "@/components/filters/EffectsFilterSection"
import {FilterSearchBar} from "@/components/filters/FilterSearchBar"
import {
  ItemGradeFilterSection,
  itemGradeValidator,
} from "@/components/filters/ItemGradeFilterSection"
import {SortDirectionFilterSection} from "@/components/filters/SortDirectionFilterSection"
import {SortKeyFilterSection} from "@/components/filters/SortKeyFilterSection"
import {GridItem} from "@/components/grid-item"
import {GridItemsList} from "@/components/grid-items-list"
import {
  BreadcrumbItem,
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
  databaseBreadcrumbItems,
} from "@/components/page-header"
import {Pagination} from "@/components/pagination"
import {PaginationContentWrapper} from "@/components/pagination-content-wrapper"
import {Filter, FilterMenu} from "@/components/pagination-filter"

import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, useNavigate} from "@tanstack/react-router"
import {fallback, zodSearchValidator} from "@tanstack/router-zod-adapter"
import {z} from "zod"

const query = graphql(`
  query EssencesPagination(
    $offset: Int!
    $limit: Int!
    $filter: EssenceFilter
    $order_by: [EssenceSort!]
  ) {
    all_essences(
      offset: $offset
      limit: $limit
      filter: $filter
      order_by: $order_by
    ) {
      total_count
      items {
        code
        name
        icon
        required_level
        grade
        is_core
        equip_type
        ...EffectsFragment
      }
    }
  }
`)

const essenceEquipOptions: ComboboxOption<EssenceEquipType>[] = [
  {
    label: "Equip: All",
    value: EssenceEquipType.All,
  },
  {
    label: "Equip: Weapons",
    value: EssenceEquipType.Weapons,
  },
  {
    label: "Equip: Armor",
    value: EssenceEquipType.Armor,
  },
]
const essenceEquipTypeValidator = z.custom<EssenceEquipType>((val) =>
  essenceEquipOptions.map((o) => o.value).includes(val),
)

const essenceSlotOptions: ComboboxOption<"core" | "meta">[] = [
  {
    label: "Core",
    value: "core",
  },
  {
    label: "Meta",
    value: "meta",
  },
]
const essenceSlotOptionsValidator = z.custom<"core" | "meta">((val) =>
  essenceSlotOptions.map((o) => o.value).includes(val),
)

type AllowedSortOptions = keyof EssenceFilter
const sortOptions: ComboboxOption<AllowedSortOptions>[] = [
  {
    label: "Added",
    value: "row_id",
  },
  {
    label: "Name",
    value: "name",
  },
  {
    label: "Required Level",
    value: "required_level",
  },
] as const
const sortKeyValidator = z.custom<AllowedSortOptions>((val) =>
  sortOptions.map((o) => o.value).includes(val),
)

const searchValidator = zodSearchValidator(
  z.object({
    page: pageValidator,
    s: searchStringValidator,
    grade: fallback(itemGradeValidator.nullable(), null).default(null),
    eet: fallback(essenceEquipTypeValidator.nullable(), null).default(null),
    slot: fallback(essenceSlotOptionsValidator.nullable(), null).default(null),
    effects: fallback(effectsValidator, []).default([]),
    sk: fallback(sortKeyValidator, "row_id").default("row_id"),
    sd: sortDirectionValidatorWithDescDefault,
  }),
)

const makeQueryOptions = (
  offset: number,
  limit: number,
  searchString: string,
  sortKey: typeof searchValidator.types.output.sk,
  sortDirection: typeof searchValidator.types.output.sd,
  grade: typeof searchValidator.types.output.grade,
  effects: typeof searchValidator.types.output.effects,
  essenceEquipType: typeof searchValidator.types.output.eet,
  slot: typeof searchValidator.types.output.slot,
) =>
  queryOptions({
    queryKey: [
      "allEssences",
      offset,
      limit,
      sortKey,
      sortDirection,
      effects,
      grade,
      essenceEquipType,
      slot,
      searchString,
    ],
    queryFn: async () =>
      gqlClient.request(query, {
        offset: offset,
        limit: limit,
        filter: {
          ...(searchString ? {name: {ilike: `%${searchString}%`}} : {}),
          ...(effects.length > 0
            ? {effects: {effect_code: {in: effects}}}
            : {}),
          ...(grade === null ? {} : {grade: {eq: grade}}),
          ...(essenceEquipType === null
            ? {}
            : {equip_type: {eq: essenceEquipType}}),
          ...(slot === null ? {} : {is_core: {eq: slot === "core"}}),
        },
        order_by: [{[sortKey]: sortDirection} as unknown as EssenceSort],
      }),
  })

export const Route = createFileRoute("/database/(essence)/essence")({
  loaderDeps: ({
    search: {
      page,
      s: searchString,
      sk: sortKey,
      sd: sortDirection,
      eet: essenceEquipType,
      slot,
      grade,
      effects,
    },
  }) => ({
    ...calculateLimitOffsetFromPage(page),
    sortKey,
    sortDirection,
    grade,
    effects,
    essenceEquipType,
    slot,
    searchString,
  }),
  loader: ({
    deps: {
      offset,
      limit,
      searchString,
      sortKey,
      sortDirection,
      grade,
      essenceEquipType,
      slot,
      effects,
    },
  }) =>
    queryClient.ensureQueryData(
      makeQueryOptions(
        offset,
        limit,
        searchString,
        sortKey,
        sortDirection,
        grade,
        effects,
        essenceEquipType,
        slot,
      ),
    ),
  component: RouteComponent,
  validateSearch: searchValidator,
})

export const essenceBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Essences",
    href: "/database/essence",
  },
]

function RouteComponent() {
  const navigate = useNavigate({from: Route.fullPath})
  const {
    page,
    s: search,
    sk: sortKey,
    sd: sortDirection,
    eet: essenceEquipType,
    grade,
    effects,
    slot,
  } = Route.useSearch()
  const {offset, limit} = calculateLimitOffsetFromPage(page)
  const {
    data: {
      all_essences: {total_count, items},
    },
  } = useSuspenseQuery(
    makeQueryOptions(
      offset,
      limit,
      search,
      sortKey,
      sortDirection,
      grade,
      effects,
      essenceEquipType,
      slot,
    ),
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs items={essenceBreadcrumbItems} />
        <PageTitle title={last(essenceBreadcrumbItems)!.label} />
      </PageHeader>

      <PaginationContentWrapper>
        <Filter>
          <FilterSearchBar navigate={navigate} value={search} />
          <FilterMenu>
            {({Section, Label}) => (
              <>
                <SortKeyFilterSection
                  Section={Section}
                  Label={Label}
                  sortKey={sortKey}
                  sortOptions={sortOptions}
                  navigate={navigate}
                />
                <SortDirectionFilterSection
                  Section={Section}
                  Label={Label}
                  direction={sortDirection}
                  navigate={navigate}
                />
                <EffectsFilterSection
                  Section={Section}
                  Label={Label}
                  effects={effects}
                  navigate={navigate}
                />
                <ItemGradeFilterSection
                  Section={Section}
                  Label={Label}
                  grade={grade}
                  navigate={navigate}
                />
                <Section>
                  <Label htmlFor="essence-equip-type">Type</Label>
                  <Combobox
                    nullable
                    id="essence-equip-type"
                    triggerClassName="col-span-2"
                    value={essenceEquipType}
                    options={essenceEquipOptions}
                    onValueChange={(value) => {
                      navigate({
                        search: (prev) => ({
                          ...prev,
                          page: 1,
                          eet: value,
                        }),
                      })
                    }}
                  />
                </Section>
                <Section>
                  <Label htmlFor="essence-slot-type">Slot</Label>
                  <Combobox
                    nullable
                    id="essence-slot-type"
                    triggerClassName="col-span-2"
                    value={slot}
                    options={essenceSlotOptions}
                    onValueChange={(value) => {
                      navigate({
                        search: (prev) => ({
                          ...prev,
                          page: 1,
                          slot: value,
                        }),
                      })
                    }}
                  />
                </Section>
              </>
            )}
          </FilterMenu>
        </Filter>
        <GridItemsList items={items}>
          {(items) =>
            items.map((essence) => (
              <GridItem.Item
                key={essence.code}
                from={Route.fullPath}
                to="$code"
                params={{code: essence.code}}
              >
                <GridItem.Icon
                  iconName={essence.icon}
                  itemGrade={essence.grade}
                />
                <GridItem.Details>
                  <GridItem.Name>{essence.name}</GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Item-Lv. ${essence.required_level}`,
                      essence.is_core ? "Core" : "Meta",
                      essenceEquipTypeToString(essence.equip_type),
                    ]}
                  />
                  <GridItem.Effects effects={essence.effects} />
                </GridItem.Details>
              </GridItem.Item>
            ))
          }
        </GridItemsList>
        <Pagination
          currentPage={page}
          totalItemsCount={total_count}
          perPage={limit}
        />
      </PaginationContentWrapper>
    </>
  )
}
