import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {
  characterClassStringFromObject,
  genderToString,
} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {pageValidator} from "@/utils/search-validators/page-validator"
import {searchStringValidator} from "@/utils/search-validators/search-string-validator"
import {sortDirectionValidatorWithDescDefault} from "@/utils/search-validators/sort-direction-validators"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {AccessorySort, AccessoryType} from "@/gql/graphql"

import {Combobox, ComboboxOption} from "@/components/combobox"
import {
  CharacterClassFilterSection,
  characterClassValidators,
} from "@/components/filters/CharacterClassFilterSection"
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
  query AccessoriesPagination(
    $offset: Int!
    $limit: Int!
    $filter: AccessoryFilter
    $order_by: [AccessorySort!]
  ) {
    all_accessories(
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
        level_land
        level_sea
        grade
        duration
        gender
        accessory_type
        duration
        ...CharacterClassFragment
        ...EffectsFragment
      }
    }
  }
`)

const accessoryTypeOptions: ComboboxOption<AccessoryType>[] = [
  {
    label: "Necklace",
    value: AccessoryType.Necklace,
  },
  {
    label: "Earrings",
    value: AccessoryType.Earring,
  },
  {
    label: "Ring",
    value: AccessoryType.Ring,
  },
]
const accessoryTypeValidator = z.custom<AccessoryType>((val) =>
  accessoryTypeOptions.map((o) => o.value).includes(val),
)

type AllowedSortOptions = keyof AccessorySort
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
    label: "Level Land",
    value: "level_land",
  },
  {
    label: "Level Sea",
    value: "level_sea",
  },
] as const
const sortKeyValidator = z.custom<AllowedSortOptions>((val) =>
  sortOptions.map((o) => o.value).includes(val),
)

const searchValidator = zodSearchValidator(
  z.object({
    page: pageValidator,
    s: searchStringValidator,
    cc: fallback(characterClassValidators.nullable(), null).default(null),
    grade: fallback(itemGradeValidator.nullable(), null).default(null),
    at: fallback(accessoryTypeValidator.nullable(), null).default(null),
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
  characterClass: typeof searchValidator.types.output.cc,
  grade: typeof searchValidator.types.output.grade,
  effects: typeof searchValidator.types.output.effects,
  accessoryType: typeof searchValidator.types.output.at,
) =>
  queryOptions({
    queryKey: [
      "allAccessories",
      offset,
      limit,
      sortKey,
      sortDirection,
      characterClass,
      effects,
      grade,
      accessoryType,
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
          ...(characterClass === null ? {} : {[characterClass]: {eq: true}}),
          ...(grade === null ? {} : {grade: {eq: grade}}),
          ...(accessoryType === null
            ? {}
            : {accessory_type: {eq: accessoryType}}),
        },
        order_by: [{[sortKey]: sortDirection} as unknown as AccessorySort],
      }),
  })

export const Route = createFileRoute("/database/(extra-equipment)/accessory")({
  loaderDeps: ({
    search: {
      page,
      s: searchString,
      sk: sortKey,
      sd: sortDirection,
      cc: characterClass,
      at: accessoryType,
      grade,
      effects,
    },
  }) => ({
    ...calculateLimitOffsetFromPage(page),
    sortKey,
    sortDirection,
    characterClass,
    grade,
    effects,
    accessoryType,
    searchString,
  }),
  loader: ({
    deps: {
      offset,
      limit,
      searchString,
      sortKey,
      sortDirection,
      characterClass,
      grade,
      accessoryType,
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
        characterClass,
        grade,
        effects,
        accessoryType,
      ),
    ),
  component: RouteComponent,
  validateSearch: searchValidator,
})

export const accessoryBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Accessories",
    href: "/database/accessory",
  },
]

function RouteComponent() {
  const navigate = useNavigate({from: Route.fullPath})
  const {
    page,
    s: search,
    sk: sortKey,
    sd: sortDirection,
    cc: characterClass,
    at: accessoryType,
    grade,
    effects,
  } = Route.useSearch()
  const {offset, limit} = calculateLimitOffsetFromPage(page)
  const {
    data: {
      all_accessories: {total_count, items},
    },
  } = useSuspenseQuery(
    makeQueryOptions(
      offset,
      limit,
      search,
      sortKey,
      sortDirection,
      characterClass,
      grade,
      effects,
      accessoryType,
    ),
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs items={accessoryBreadcrumbItems} />
        <PageTitle title={last(accessoryBreadcrumbItems)!.label} />
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
                <CharacterClassFilterSection
                  Section={Section}
                  Label={Label}
                  cc={characterClass}
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
                  <Label htmlFor="accessory-type">Type</Label>
                  <Combobox
                    nullable
                    id="accessory-type"
                    triggerClassName="col-span-2"
                    value={accessoryType}
                    options={accessoryTypeOptions}
                    onValueChange={(value) => {
                      navigate({
                        search: (prev) => ({
                          ...prev,
                          page: 1,
                          at: value,
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
            items.map((accessory) => (
              <GridItem.Item
                key={accessory.code}
                from={Route.fullPath}
                to="$code"
                params={{code: accessory.code}}
              >
                <GridItem.Icon
                  iconName={accessory.icon}
                  itemGrade={accessory.grade}
                />
                <GridItem.Details>
                  <GridItem.Name duration={accessory.duration}>
                    {accessory.name}
                  </GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${accessory.level_land}/${accessory.level_sea}`,
                      genderToString(accessory.gender),
                      characterClassStringFromObject(accessory),
                    ]}
                  />
                  <GridItem.Effects effects={accessory.effects} />
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
