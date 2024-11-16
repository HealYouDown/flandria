import {shipClassFromObject} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {
  ShipHeadMastFilter,
  ShipHeadMastPaginationQuery,
  ShipHeadMastSort,
} from "@/gql/graphql"

import {EffectsFilterSection} from "@/components/filters/EffectsFilterSection"
import {FilterSearchBar} from "@/components/filters/FilterSearchBar"
import {ItemGradeFilterSection} from "@/components/filters/ItemGradeFilterSection"
import {ShipClassFilterSection} from "@/components/filters/ShipClassFilterSection"
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

import {makeShipRoute} from "../-make-pagination-route"
import {makeQueryOptionsFactory} from "../-pagination-query-options"
import {sortOptions} from "../-pagination-search-validator"

import {useSuspenseQuery} from "@tanstack/react-query"
import {useNavigate} from "@tanstack/react-router"

const query = graphql(`
  query ShipHeadMastPagination(
    $offset: Int!
    $limit: Int!
    $filter: ShipHeadMastFilter
    $order_by: [ShipHeadMastSort!]
  ) {
    all_ship_head_masts(
      offset: $offset
      limit: $limit
      filter: $filter
      order_by: $order_by
    ) {
      total_count
      items {
        ...ShipPaginationFragment
      }
    }
  }
`)

const makeQueryOptions = makeQueryOptionsFactory<
  ShipHeadMastPaginationQuery,
  ShipHeadMastFilter,
  ShipHeadMastSort
>({queryKeyPrefix: "allShipHeadMasts", query: query})

export const Route = makeShipRoute<
  ShipHeadMastPaginationQuery,
  ShipHeadMastFilter,
  ShipHeadMastSort
>({
  path: "ship_head_mast",
  makeQueryOptions: makeQueryOptions,
  component: RouteComponent,
})

export const shipHeadMastBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Ship Head Masts",
    href: "/database/ship_head_mast",
  },
]

export function RouteComponent() {
  const navigate = useNavigate({from: Route.fullPath})
  const {
    page,
    s: search,
    sk: sortKey,
    sd: sortDirection,
    sc: shipClass,
    grade,
    effects,
  } = Route.useSearch()
  const {offset, limit} = calculateLimitOffsetFromPage(page)
  const {
    data: {
      all_ship_head_masts: {total_count, items},
    },
  } = useSuspenseQuery(
    makeQueryOptions(
      offset,
      limit,
      search,
      sortKey,
      sortDirection,
      shipClass,
      grade,
      effects,
    ),
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs items={shipHeadMastBreadcrumbItems} />
        <PageTitle title={last(shipHeadMastBreadcrumbItems)!.label} />
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
                <ShipClassFilterSection
                  Section={Section}
                  Label={Label}
                  cc={shipClass}
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
              </>
            )}
          </FilterMenu>
        </Filter>
        <GridItemsList items={items}>
          {(items) =>
            items.map((ship_head_mast) => (
              <GridItem.Item
                key={ship_head_mast.code}
                from="/database/ship_head_mast"
                to="$code"
                params={{code: ship_head_mast.code}}
              >
                <GridItem.Icon
                  iconName={ship_head_mast.icon}
                  itemGrade={ship_head_mast.grade}
                />
                <GridItem.Details>
                  <GridItem.Name duration={ship_head_mast.duration}>
                    {ship_head_mast.name}
                  </GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${ship_head_mast.level_sea}`,
                      shipClassFromObject(ship_head_mast),
                    ]}
                  />
                  <GridItem.Effects effects={ship_head_mast.effects} />
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
