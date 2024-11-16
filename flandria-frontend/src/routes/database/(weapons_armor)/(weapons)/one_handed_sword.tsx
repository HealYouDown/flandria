import {characterClassStringFromObject} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {
  OneHandedSwordFilter,
  OneHandedSwordSort,
  OneHandedSwordsPaginationQuery,
} from "@/gql/graphql"

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
  query OneHandedSwordsPagination(
    $offset: Int!
    $limit: Int!
    $filter: OneHandedSwordFilter
    $order_by: [OneHandedSwordSort!]
  ) {
    all_one_handed_swords(
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
  OneHandedSwordsPaginationQuery,
  OneHandedSwordFilter,
  OneHandedSwordSort
>({queryKeyPrefix: "allOneHandedSwords", query: query})

export const oneHandedSwordsBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "One-handed Swords",
    href: "/database/one_handed_sword",
  },
]

export const Route = makeWeaponsArmorRoute<
  OneHandedSwordsPaginationQuery,
  OneHandedSwordFilter,
  OneHandedSwordSort
>({
  path: "one_handed_sword",
  makeQueryOptions: makeQueryOptions,
  component: RouteComponent,
})

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
      all_one_handed_swords: {total_count, items},
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
        <PageHeaderBreadcrumbs items={oneHandedSwordsBreadcrumbItems} />
        <PageTitle title={last(oneHandedSwordsBreadcrumbItems)!.label} />
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
            items.map((one_handed_sword) => (
              <GridItem.Item
                key={one_handed_sword.code}
                from="/database/one_handed_sword"
                to="$code"
                params={{code: one_handed_sword.code}}
              >
                <GridItem.Icon
                  iconName={one_handed_sword.icon}
                  itemGrade={one_handed_sword.grade}
                />
                <GridItem.Details>
                  <GridItem.Name duration={one_handed_sword.duration}>
                    {one_handed_sword.name}
                  </GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${one_handed_sword.level_land}/${one_handed_sword.level_sea}`,
                      characterClassStringFromObject(one_handed_sword),
                    ]}
                  />
                  <GridItem.Effects effects={one_handed_sword.effects} />
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
