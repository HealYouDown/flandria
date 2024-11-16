import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {pageValidator} from "@/utils/search-validators/page-validator"
import {searchStringValidator} from "@/utils/search-validators/search-string-validator"
import {sortDirectionValidatorWithAscDefault} from "@/utils/search-validators/sort-direction-validators"

import {graphql} from "@/gql"
import {NpcSort} from "@/gql/graphql"

import {ComboboxOption} from "@/components/combobox"
import {FilterSearchBar} from "@/components/filters/FilterSearchBar"
import {
  LandSeaFilterSection,
  landSeaValidator,
} from "@/components/filters/LandSeaFilterSection"
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
  query NPCsPagination(
    $offset: Int!
    $limit: Int!
    $filter: NpcFilter
    $order_by: [NpcSort!]
  ) {
    all_npcs(
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
        level
        is_sea
        grade
      }
    }
  }
`)

type AllowedSortOptions = keyof NpcSort
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
    area: fallback(landSeaValidator.nullable(), null).default(null),
    sk: fallback(sortKeyValidator, "row_id").default("row_id"),
    sd: sortDirectionValidatorWithAscDefault,
  }),
)

const makeQueryOptions = (
  offset: number,
  limit: number,
  searchString: string,
  area: typeof searchValidator.types.output.area,
  sortKey: typeof searchValidator.types.output.sk,
  sortDirection: typeof searchValidator.types.output.sd,
) =>
  queryOptions({
    queryKey: [
      "allNpcs",
      offset,
      limit,
      area,
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
          ...(area !== null ? {is_sea: {eq: area === "sea"}} : {}),
        },
        order_by: [{[sortKey]: sortDirection} as unknown as NpcSort],
      }),
  })

export const Route = createFileRoute("/database/(actors)/npc")({
  loaderDeps: ({
    search: {page, s: searchString, area, sk: sortKey, sd: sortDirection},
  }) => ({
    ...calculateLimitOffsetFromPage(page),
    area,
    sortKey,
    sortDirection,
    searchString,
  }),
  loader: ({
    deps: {offset, limit, searchString, area, sortKey, sortDirection},
  }) =>
    queryClient.ensureQueryData(
      makeQueryOptions(
        offset,
        limit,
        searchString,
        area,
        sortKey,
        sortDirection,
      ),
    ),
  component: RouteComponent,
  validateSearch: searchValidator,
})

export const npcBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "NPCs",
    href: "/database/npc",
  },
]

function RouteComponent() {
  const navigate = useNavigate({from: Route.fullPath})
  const {
    page,
    s: search,
    area,
    sk: sortKey,
    sd: sortDirection,
  } = Route.useSearch()
  const {offset, limit} = calculateLimitOffsetFromPage(page)
  const {
    data: {
      all_npcs: {total_count, items},
    },
  } = useSuspenseQuery(
    makeQueryOptions(offset, limit, search, area, sortKey, sortDirection),
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs items={npcBreadcrumbItems} />
        <PageTitle title="NPCs" />
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
                <LandSeaFilterSection
                  Section={Section}
                  Label={Label}
                  area={area}
                  navigate={navigate}
                />
              </>
            )}
          </FilterMenu>
        </Filter>
        <GridItemsList items={items}>
          {(items) =>
            items.map((npc) => (
              <GridItem.Item
                key={npc.code}
                from={Route.fullPath}
                to="$code"
                params={{code: npc.code}}
              >
                <GridItem.Icon iconName={npc.icon} actorGrade={npc.grade} />
                <GridItem.Details>
                  <GridItem.Name>{npc.name}</GridItem.Name>
                  <GridItem.Subs
                    subs={[`Lv. ${npc.level}`, npc.is_sea ? "Sea" : "Land"]}
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
