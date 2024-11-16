import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {pageValidator} from "@/utils/search-validators/page-validator"
import {searchStringValidator} from "@/utils/search-validators/search-string-validator"
import {sortDirectionValidatorWithDescDefault} from "@/utils/search-validators/sort-direction-validators"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {RandomBoxSort} from "@/gql/graphql"

import {ComboboxOption} from "@/components/combobox"
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
  query RandomBoxPagination(
    $offset: Int!
    $limit: Int!
    $filter: RandomBoxFilter
    $order_by: [RandomBoxSort!]
  ) {
    all_random_boxes(
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
        grade
        level_land
        level_sea
      }
    }
  }
`)

type AllowedSortOptions = keyof RandomBoxSort
const sortOptions: ComboboxOption<AllowedSortOptions>[] = [
  {
    label: "Added",
    value: "row_id",
  },
  {
    label: "Name",
    value: "name",
  },
] as const
const sortKeyValidator = z.custom<AllowedSortOptions>((val) =>
  sortOptions.map((o) => o.value).includes(val),
)

const searchValidator = zodSearchValidator(
  z.object({
    page: pageValidator,
    s: searchStringValidator,
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
) =>
  queryOptions({
    queryKey: [
      "allRandomBoxes",
      offset,
      limit,
      sortKey,
      sortDirection,
      searchString,
    ],
    queryFn: async () =>
      gqlClient.request(query, {
        offset: offset,
        limit: limit,
        filter: {
          ...(searchString ? {name: {ilike: `%${searchString}%`}} : {}),
        },
        order_by: [{[sortKey]: sortDirection} as unknown as RandomBoxSort],
      }),
  })

export const Route = createFileRoute("/database/(more)/random_box")({
  loaderDeps: ({
    search: {page, s: searchString, sk: sortKey, sd: sortDirection},
  }) => ({
    ...calculateLimitOffsetFromPage(page),
    sortKey,
    sortDirection,
    searchString,
  }),
  loader: ({deps: {offset, limit, searchString, sortKey, sortDirection}}) =>
    queryClient.ensureQueryData(
      makeQueryOptions(offset, limit, searchString, sortKey, sortDirection),
    ),
  component: RouteComponent,
  validateSearch: searchValidator,
})

export const randomBoxBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Random Boxes",
    href: "/database/random_box",
  },
]

function RouteComponent() {
  const navigate = useNavigate({from: Route.fullPath})
  const {page, s: search, sk: sortKey, sd: sortDirection} = Route.useSearch()
  const {offset, limit} = calculateLimitOffsetFromPage(page)
  const {
    data: {
      all_random_boxes: {total_count, items},
    },
  } = useSuspenseQuery(
    makeQueryOptions(offset, limit, search, sortKey, sortDirection),
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs items={randomBoxBreadcrumbItems} />
        <PageTitle title={last(randomBoxBreadcrumbItems)!.label} />
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
              </>
            )}
          </FilterMenu>
        </Filter>
        <GridItemsList items={items}>
          {(items) =>
            items.map((random_box) => (
              <GridItem.Item
                key={random_box.code}
                from={Route.fullPath}
                to="$code"
                params={{code: random_box.code}}
              >
                <GridItem.Icon
                  iconName={random_box.icon}
                  itemGrade={random_box.grade}
                />
                <GridItem.Details>
                  <GridItem.Name>{random_box.name}</GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${random_box.level_land}/${random_box.level_sea}`,
                    ]}
                  />
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
