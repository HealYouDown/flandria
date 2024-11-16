import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {
  characterClassStringFromObject,
  genderToString,
  productionTypeToString,
} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {pageValidator} from "@/utils/search-validators/page-validator"
import {searchStringValidator} from "@/utils/search-validators/search-string-validator"
import {sortDirectionValidatorWithAscDefault} from "@/utils/search-validators/sort-direction-validators"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {ProductionSort, SecondJobType} from "@/gql/graphql"

import {Combobox, ComboboxOption} from "@/components/combobox"
import {FilterSearchBar} from "@/components/filters/FilterSearchBar"
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
  query ProductionPagination(
    $offset: Int!
    $limit: Int!
    $filter: ProductionFilter
    $order_by: [ProductionSort!]
  ) {
    all_productions(
      offset: $offset
      limit: $limit
      filter: $filter
      order_by: $order_by
    ) {
      total_count
      items {
        code
        type
        points_required
        result_quantity
        result_item {
          name
          icon
          grade
          level_land
          level_sea
          duration
          gender
          ...CharacterClassFragment
          ...EffectsFragment
        }
      }
    }
  }
`)

type AllowedSortOptions = keyof ProductionSort
const sortOptions: ComboboxOption<AllowedSortOptions>[] = [
  {
    label: "Added",
    value: "row_id",
  },
  {
    label: "Required Points",
    value: "points_required",
  },
] as const
const sortKeyValidator = z.custom<AllowedSortOptions>((val) =>
  sortOptions.map((o) => o.value).includes(val),
)

const secondJobTypeOptions: ComboboxOption<SecondJobType>[] = [
  {
    label: productionTypeToString(SecondJobType.Alchemist),
    value: SecondJobType.Alchemist,
  },
  {
    label: productionTypeToString(SecondJobType.ArmorSmith),
    value: SecondJobType.ArmorSmith,
  },
  {
    label: productionTypeToString(SecondJobType.WeaponSmith),
    value: SecondJobType.WeaponSmith,
  },
  {
    label: productionTypeToString(SecondJobType.Workmanship),
    value: SecondJobType.Workmanship,
  },
  {
    label: productionTypeToString(SecondJobType.Essence),
    value: SecondJobType.Essence,
  },
]
const secondJobTypeValidator = z.custom<SecondJobType>((val) =>
  secondJobTypeOptions.map((o) => o.value).includes(val),
)

const searchValidator = zodSearchValidator(
  z.object({
    page: pageValidator,
    s: searchStringValidator,
    sk: fallback(sortKeyValidator, "row_id").default("row_id"),
    sd: sortDirectionValidatorWithAscDefault,
    type: fallback(secondJobTypeValidator.nullable(), null).default(null),
  }),
)

const makeQueryOptions = (
  offset: number,
  limit: number,
  searchString: string,
  sortKey: typeof searchValidator.types.output.sk,
  sortDirection: typeof searchValidator.types.output.sd,
  type: typeof searchValidator.types.output.type,
) =>
  queryOptions({
    queryKey: [
      "allProductions",
      offset,
      limit,
      sortKey,
      sortDirection,
      type,
      searchString,
    ],
    queryFn: async () =>
      gqlClient.request(query, {
        offset: offset,
        limit: limit,
        filter: {
          ...(searchString
            ? {result_item: {name: {ilike: `%${searchString}%`}}}
            : {}),
          ...(type ? {type: {eq: type}} : {}),
        },
        order_by: [{[sortKey]: sortDirection} as unknown as ProductionSort],
      }),
  })

export const Route = createFileRoute("/database/(crafting)/production")({
  loaderDeps: ({
    search: {page, s: searchString, sk: sortKey, sd: sortDirection, type},
  }) => ({
    ...calculateLimitOffsetFromPage(page),
    sortKey,
    sortDirection,
    searchString,
    type,
  }),
  loader: ({
    deps: {offset, limit, searchString, sortKey, sortDirection, type},
  }) =>
    queryClient.ensureQueryData(
      makeQueryOptions(
        offset,
        limit,
        searchString,
        sortKey,
        sortDirection,
        type,
      ),
    ),
  component: RouteComponent,
  validateSearch: searchValidator,
})

export const productionBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "2nd Job",
    href: "/database/production",
  },
]

function RouteComponent() {
  const navigate = useNavigate({from: Route.fullPath})
  const {
    page,
    s: search,
    sk: sortKey,
    sd: sortDirection,
    type,
  } = Route.useSearch()
  const {offset, limit} = calculateLimitOffsetFromPage(page)
  const {
    data: {
      all_productions: {total_count, items},
    },
  } = useSuspenseQuery(
    makeQueryOptions(offset, limit, search, sortKey, sortDirection, type),
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs items={productionBreadcrumbItems} />
        <PageTitle title={last(productionBreadcrumbItems)!.label} />
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
                <Section>
                  <Label htmlFor="2nd-job-type">Type</Label>
                  <Combobox
                    nullable
                    id="2nd-job-type"
                    triggerClassName="col-span-2"
                    value={type}
                    options={secondJobTypeOptions}
                    onValueChange={(value) => {
                      navigate({
                        search: (prev) => ({
                          ...prev,
                          page: 1,
                          type: value,
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
            items.map((production) => {
              const {result_item: item} = production
              const subs = []

              if (production.result_quantity > 1) {
                subs.push(`${production.result_quantity}x`)
              }

              if (item.level_land !== null && item.level_sea === null) {
                subs.push(`Land Lv. ${item.level_land}`)
              } else if (item.level_land === null && item.level_sea !== null) {
                subs.push(`Sea Lv. ${item.level_sea}`)
              } else if (item.level_land !== null && item.level_sea !== null) {
                subs.push(`Lv. ${item.level_land}/${item.level_sea}`)
              }

              if (item.gender) {
                subs.push(genderToString(item.gender))
              }
              subs.push(characterClassStringFromObject(item))

              return (
                <GridItem.Item
                  key={production.code}
                  from={Route.fullPath}
                  to="$code"
                  params={{code: production.code}}
                >
                  <GridItem.Icon iconName={item.icon} itemGrade={item.grade} />
                  <GridItem.Details>
                    <GridItem.Name duration={item.duration}>
                      {production.result_item.name}
                    </GridItem.Name>
                    <GridItem.Subs subs={subs} />
                    <GridItem.Effects effects={item.effects} />
                  </GridItem.Details>
                </GridItem.Item>
              )
            })
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
