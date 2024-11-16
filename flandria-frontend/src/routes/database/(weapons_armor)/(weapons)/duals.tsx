import {characterClassStringFromObject} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {DualsFilter, DualsSort, DualssPaginationQuery} from "@/gql/graphql"

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
  query DualssPagination(
    $offset: Int!
    $limit: Int!
    $filter: DualsFilter
    $order_by: [DualsSort!]
  ) {
    all_duals(
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
  DualssPaginationQuery,
  DualsFilter,
  DualsSort
>({queryKeyPrefix: "allDuals", query: query})

export const Route = makeWeaponsArmorRoute<
  DualssPaginationQuery,
  DualsFilter,
  DualsSort
>({
  path: "duals",
  makeQueryOptions: makeQueryOptions,
  component: RouteComponent,
})

export const dualsBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Duals",
    href: "/database/duals",
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
      all_duals: {total_count, items},
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
        <PageHeaderBreadcrumbs items={dualsBreadcrumbItems} />
        <PageTitle title={last(dualsBreadcrumbItems)!.label} />
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
            items.map((duals) => (
              <GridItem.Item
                key={duals.code}
                from="/database/duals"
                to="$code"
                params={{code: duals.code}}
              >
                <GridItem.Icon iconName={duals.icon} itemGrade={duals.grade} />
                <GridItem.Details>
                  <GridItem.Name duration={duals.duration}>
                    {duals.name}
                  </GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${duals.level_land}/${duals.level_sea}`,
                      characterClassStringFromObject(duals),
                    ]}
                  />
                  <GridItem.Effects effects={duals.effects} />
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
