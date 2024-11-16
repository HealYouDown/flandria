import {characterClassStringFromObject} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {RapierFilter, RapierSort, RapiersPaginationQuery} from "@/gql/graphql"

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
  query RapiersPagination(
    $offset: Int!
    $limit: Int!
    $filter: RapierFilter
    $order_by: [RapierSort!]
  ) {
    all_rapiers(
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
  RapiersPaginationQuery,
  RapierFilter,
  RapierSort
>({queryKeyPrefix: "allRapiers", query: query})

export const Route = makeWeaponsArmorRoute<
  RapiersPaginationQuery,
  RapierFilter,
  RapierSort
>({
  path: "rapier",
  makeQueryOptions: makeQueryOptions,
  component: RouteComponent,
})

export const rapierBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Rapiers",
    href: "/database/rapier",
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
      all_rapiers: {total_count, items},
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
        <PageHeaderBreadcrumbs items={rapierBreadcrumbItems} />
        <PageTitle title={last(rapierBreadcrumbItems)!.label} />
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
            items.map((rapier) => (
              <GridItem.Item
                key={rapier.code}
                from="/database/rapier"
                to="$code"
                params={{code: rapier.code}}
              >
                <GridItem.Icon
                  iconName={rapier.icon}
                  itemGrade={rapier.grade}
                />
                <GridItem.Details>
                  <GridItem.Name duration={rapier.duration}>
                    {rapier.name}
                  </GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${rapier.level_land}/${rapier.level_sea}`,
                      characterClassStringFromObject(rapier),
                    ]}
                  />
                  <GridItem.Effects effects={rapier.effects} />
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
