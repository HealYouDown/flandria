import {characterClassStringFromObject} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {CariadFilter, CariadSort, CariadsPaginationQuery} from "@/gql/graphql"

import {CharacterClassFilterSection} from "@/components/filters/CharacterClassFilterSection"
import {EffectsFilterSection} from "@/components/filters/EffectsFilterSection"
import {FilterSearchBar} from "@/components/filters/FilterSearchBar"
import {ItemGradeFilterSection} from "@/components/filters/ItemGradeFilterSection"
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

import {makeWeaponsArmorRoute} from "../-make-pagination-route"
import {makeQueryOptionsFactory} from "../-pagination-query-options"
import {sortOptions} from "../-pagination-search-validator"

import {useSuspenseQuery} from "@tanstack/react-query"
import {useNavigate} from "@tanstack/react-router"

const query = graphql(`
  query CariadsPagination(
    $offset: Int!
    $limit: Int!
    $filter: CariadFilter
    $order_by: [CariadSort!]
  ) {
    all_cariads(
      offset: $offset
      limit: $limit
      filter: $filter
      order_by: $order_by
    ) {
      total_count
      items {
        ...WeaponPaginationFragment
      }
    }
  }
`)

const makeQueryOptions = makeQueryOptionsFactory<
  CariadsPaginationQuery,
  CariadFilter,
  CariadSort
>({queryKeyPrefix: "allCariads", query: query})

export const Route = makeWeaponsArmorRoute<
  CariadsPaginationQuery,
  CariadFilter,
  CariadSort
>({
  path: "cariad",
  makeQueryOptions: makeQueryOptions,
  component: RouteComponent,
})

export const cariadBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Cariads",
    href: "/database/cariad",
  },
]

export function RouteComponent() {
  const navigate = useNavigate({from: Route.fullPath})
  const {
    page,
    s: search,
    sk: sortKey,
    sd: sortDirection,
    cc: characterClass,
    grade,
    effects,
  } = Route.useSearch()
  const {offset, limit} = calculateLimitOffsetFromPage(page)
  const {
    data: {
      all_cariads: {total_count, items},
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
    ),
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs items={cariadBreadcrumbItems} />
        <PageTitle title={last(cariadBreadcrumbItems)!.label} />
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
              </>
            )}
          </FilterMenu>
        </Filter>
        <GridItemsList items={items}>
          {(items) =>
            items.map((cariad) => (
              <GridItem.Item
                key={cariad.code}
                from="/database/cariad"
                to="$code"
                params={{code: cariad.code}}
              >
                <GridItem.Icon
                  iconName={cariad.icon}
                  itemGrade={cariad.grade}
                />
                <GridItem.Details>
                  <GridItem.Name duration={cariad.duration}>
                    {cariad.name}
                  </GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${cariad.level_land}/${cariad.level_sea}`,
                      characterClassStringFromObject(cariad),
                    ]}
                  />
                  <GridItem.Effects effects={cariad.effects} />
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
