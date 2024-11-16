import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {pageValidator} from "@/utils/search-validators/page-validator"
import {searchStringValidator} from "@/utils/search-validators/search-string-validator"
import {sortDirectionValidatorWithDescDefault} from "@/utils/search-validators/sort-direction-validators"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {EssenceHelpSort} from "@/gql/graphql"

import {ComboboxOption} from "@/components/combobox"
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
  query EssenceHelpItemsPagination(
    $offset: Int!
    $limit: Int!
    $filter: EssenceHelpFilter
    $order_by: [EssenceHelpSort!]
  ) {
    all_essence_help_items(
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
      }
    }
  }
`)

type AllowedSortOptions = keyof EssenceHelpSort
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
    grade: fallback(itemGradeValidator.nullable(), null).default(null),
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
) =>
  queryOptions({
    queryKey: [
      "allEssenceHelpItems",
      offset,
      limit,
      sortKey,
      sortDirection,
      grade,
      searchString,
    ],
    queryFn: async () =>
      gqlClient.request(query, {
        offset: offset,
        limit: limit,
        filter: {
          ...(searchString ? {name: {ilike: `%${searchString}%`}} : {}),
          ...(grade === null ? {} : {grade: {eq: grade}}),
        },
        order_by: [{[sortKey]: sortDirection} as unknown as EssenceHelpSort],
      }),
  })

export const Route = createFileRoute("/database/(essence)/essence_help")({
  loaderDeps: ({
    search: {page, s: searchString, sk: sortKey, sd: sortDirection, grade},
  }) => ({
    ...calculateLimitOffsetFromPage(page),
    sortKey,
    sortDirection,
    grade,
    searchString,
  }),
  loader: ({
    deps: {offset, limit, searchString, sortKey, sortDirection, grade},
  }) =>
    queryClient.ensureQueryData(
      makeQueryOptions(
        offset,
        limit,
        searchString,
        sortKey,
        sortDirection,
        grade,
      ),
    ),
  component: RouteComponent,
  validateSearch: searchValidator,
})

export const essenceHelpBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Essence Help Items",
    href: "/database/essence_help",
  },
]

function RouteComponent() {
  const navigate = useNavigate({from: Route.fullPath})
  const {
    page,
    s: search,
    sk: sortKey,
    sd: sortDirection,
    grade,
  } = Route.useSearch()
  const {offset, limit} = calculateLimitOffsetFromPage(page)
  const {
    data: {
      all_essence_help_items: {total_count, items},
    },
  } = useSuspenseQuery(
    makeQueryOptions(offset, limit, search, sortKey, sortDirection, grade),
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs items={essenceHelpBreadcrumbItems} />
        <PageTitle title={last(essenceHelpBreadcrumbItems)!.label} />
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
                <ItemGradeFilterSection
                  Section={Section}
                  Label={Label}
                  grade={grade}
                  navigate={navigate}
                />
              </>
            )}
          </FilterMenu>
        </Filter>
        <GridItemsList items={items}>
          {(items) =>
            items.map((essence_help_item) => (
              <GridItem.Item
                key={essence_help_item.code}
                from={Route.fullPath}
                to="$code"
                params={{code: essence_help_item.code}}
              >
                <GridItem.Icon
                  iconName={essence_help_item.icon}
                  itemGrade={essence_help_item.grade}
                />
                <GridItem.Details>
                  <GridItem.Name>{essence_help_item.name}</GridItem.Name>
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
