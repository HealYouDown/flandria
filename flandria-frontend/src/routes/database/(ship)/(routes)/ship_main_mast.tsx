import {shipClassFromObject} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {
  ShipMainMastFilter,
  ShipMainMastPaginationQuery,
  ShipMainMastSort,
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
  query ShipMainMastPagination(
    $offset: Int!
    $limit: Int!
    $filter: ShipMainMastFilter
    $order_by: [ShipMainMastSort!]
  ) {
    all_ship_main_masts(
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
  ShipMainMastPaginationQuery,
  ShipMainMastFilter,
  ShipMainMastSort
>({queryKeyPrefix: "allShipMainMasts", query: query})

export const Route = makeShipRoute<
  ShipMainMastPaginationQuery,
  ShipMainMastFilter,
  ShipMainMastSort
>({
  path: "ship_main_mast",
  makeQueryOptions: makeQueryOptions,
  component: RouteComponent,
})

export const shipMainMastBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Ship Main Masts",
    href: "/database/ship_main_mast",
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
      all_ship_main_masts: {total_count, items},
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
        <PageHeaderBreadcrumbs items={shipMainMastBreadcrumbItems} />
        <PageTitle title={last(shipMainMastBreadcrumbItems)!.label} />
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
            items.map((ship_main_mast) => (
              <GridItem.Item
                key={ship_main_mast.code}
                from="/database/ship_main_mast"
                to="$code"
                params={{code: ship_main_mast.code}}
              >
                <GridItem.Icon
                  iconName={ship_main_mast.icon}
                  itemGrade={ship_main_mast.grade}
                />
                <GridItem.Details>
                  <GridItem.Name duration={ship_main_mast.duration}>
                    {ship_main_mast.name}
                  </GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${ship_main_mast.level_sea}`,
                      shipClassFromObject(ship_main_mast),
                    ]}
                  />
                  <GridItem.Effects effects={ship_main_mast.effects} />
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
