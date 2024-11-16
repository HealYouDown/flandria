import {shipClassFromObject} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {
  ShipSpecialWeaponFilter,
  ShipSpecialWeaponPaginationQuery,
  ShipSpecialWeaponSort,
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
  query ShipSpecialWeaponPagination(
    $offset: Int!
    $limit: Int!
    $filter: ShipSpecialWeaponFilter
    $order_by: [ShipSpecialWeaponSort!]
  ) {
    all_ship_special_weapons(
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
  ShipSpecialWeaponPaginationQuery,
  ShipSpecialWeaponFilter,
  ShipSpecialWeaponSort
>({queryKeyPrefix: "allShipSpecialWeapons", query: query})

export const Route = makeShipRoute<
  ShipSpecialWeaponPaginationQuery,
  ShipSpecialWeaponFilter,
  ShipSpecialWeaponSort
>({
  path: "ship_special_weapon",
  makeQueryOptions: makeQueryOptions,
  component: RouteComponent,
})

export const shipSpecialWeaponBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Ship Special Weapons",
    href: "/database/ship_special_weapon",
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
      all_ship_special_weapons: {total_count, items},
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
        <PageHeaderBreadcrumbs items={shipSpecialWeaponBreadcrumbItems} />
        <PageTitle title={last(shipSpecialWeaponBreadcrumbItems)!.label} />
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
            items.map((ship_special_weapon) => (
              <GridItem.Item
                key={ship_special_weapon.code}
                from="/database/ship_special_weapon"
                to="$code"
                params={{code: ship_special_weapon.code}}
              >
                <GridItem.Icon
                  iconName={ship_special_weapon.icon}
                  itemGrade={ship_special_weapon.grade}
                />
                <GridItem.Details>
                  <GridItem.Name duration={ship_special_weapon.duration}>
                    {ship_special_weapon.name}
                  </GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${ship_special_weapon.level_sea}`,
                      shipClassFromObject(ship_special_weapon),
                    ]}
                  />
                  <GridItem.Effects effects={ship_special_weapon.effects} />
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
