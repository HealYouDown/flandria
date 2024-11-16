import {shipClassFromObject} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {
  ShipNormalWeaponFilter,
  ShipNormalWeaponPaginationQuery,
  ShipNormalWeaponSort,
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
  query ShipNormalWeaponPagination(
    $offset: Int!
    $limit: Int!
    $filter: ShipNormalWeaponFilter
    $order_by: [ShipNormalWeaponSort!]
  ) {
    all_ship_normal_weapons(
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
  ShipNormalWeaponPaginationQuery,
  ShipNormalWeaponFilter,
  ShipNormalWeaponSort
>({queryKeyPrefix: "allShipNormalWeapons", query: query})

export const Route = makeShipRoute<
  ShipNormalWeaponPaginationQuery,
  ShipNormalWeaponFilter,
  ShipNormalWeaponSort
>({
  path: "ship_normal_weapon",
  makeQueryOptions: makeQueryOptions,
  component: RouteComponent,
})

export const shipNormalWeaponBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Ship Weapons",
    href: "/database/ship_normal_weapon",
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
      all_ship_normal_weapons: {total_count, items},
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
        <PageHeaderBreadcrumbs items={shipNormalWeaponBreadcrumbItems} />
        <PageTitle title={last(shipNormalWeaponBreadcrumbItems)!.label} />
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
            items.map((ship_normal_weapon) => (
              <GridItem.Item
                key={ship_normal_weapon.code}
                from="/database/ship_normal_weapon"
                to="$code"
                params={{code: ship_normal_weapon.code}}
              >
                <GridItem.Icon
                  iconName={ship_normal_weapon.icon}
                  itemGrade={ship_normal_weapon.grade}
                />
                <GridItem.Details>
                  <GridItem.Name duration={ship_normal_weapon.duration}>
                    {ship_normal_weapon.name}
                  </GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${ship_normal_weapon.level_sea}`,
                      shipClassFromObject(ship_normal_weapon),
                    ]}
                  />
                  <GridItem.Effects effects={ship_normal_weapon.effects} />
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
