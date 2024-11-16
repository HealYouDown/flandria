import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {monsterGradeToString} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {pageValidator} from "@/utils/search-validators/page-validator"
import {searchStringValidator} from "@/utils/search-validators/search-string-validator"
import {sortDirectionValidatorWithAscDefault} from "@/utils/search-validators/sort-direction-validators"

import {graphql} from "@/gql"
import {ActorGrade, MonsterSort} from "@/gql/graphql"

import {Combobox, ComboboxOption} from "@/components/combobox"
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
  query MonstersPagination(
    $offset: Int!
    $limit: Int!
    $filter: MonsterFilter
    $order_by: [MonsterSort!]
  ) {
    all_monsters(
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

const gradeFilterOptions: ComboboxOption<ActorGrade>[] = [
  {
    label: "Normal",
    value: ActorGrade.Normal,
  },
  {
    label: "Elite",
    value: ActorGrade.Elite,
  },
  {
    label: "Mini-Boss",
    value: ActorGrade.MiniBoss,
  },
  {
    label: "Boss",
    value: ActorGrade.Boss,
  },
] as const
const actorGradeValidator = z.custom<ActorGrade>((val) =>
  gradeFilterOptions.map((o) => o.value).includes(val),
)

type AllowedSortOptions = keyof MonsterSort
const sortOptions: ComboboxOption<AllowedSortOptions>[] = [
  {
    label: "Added",
    value: "row_id",
  },
  {
    label: "Name",
    value: "name",
  },
  {
    label: "Level",
    value: "level",
  },
  {
    label: "HP",
    value: "health_points",
  },
  {
    label: "Experience",
    value: "experience",
  },
] as const
const sortKeyValidator = z.custom<AllowedSortOptions>((val) =>
  sortOptions.map((o) => o.value).includes(val),
)

const searchValidator = zodSearchValidator(
  z.object({
    page: pageValidator,
    s: searchStringValidator,
    grade: fallback(actorGradeValidator.nullable(), null).default(null),
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
  grade: typeof searchValidator.types.output.grade,
  sortKey: typeof searchValidator.types.output.sk,
  sortDirection: typeof searchValidator.types.output.sd,
) =>
  queryOptions({
    queryKey: [
      "allMonsters",
      offset,
      limit,
      area,
      grade,
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
          ...(grade !== null ? {grade: {eq: grade}} : {}),
        },
        order_by: [{[sortKey]: sortDirection} as unknown as MonsterSort],
      }),
  })

export const Route = createFileRoute("/database/(actors)/monster")({
  loaderDeps: ({
    search: {
      page,
      s: searchString,
      area,
      grade,
      sk: sortKey,
      sd: sortDirection,
    },
  }) => ({
    ...calculateLimitOffsetFromPage(page),
    area,
    grade,
    sortKey,
    sortDirection,
    searchString,
  }),
  loader: ({
    deps: {offset, limit, searchString, area, grade, sortKey, sortDirection},
  }) =>
    queryClient.ensureQueryData(
      makeQueryOptions(
        offset,
        limit,
        searchString,
        area,
        grade,
        sortKey,
        sortDirection,
      ),
    ),
  component: RouteComponent,
  validateSearch: searchValidator,
})

export const monsterBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Monsters",
    href: "/database/monster",
  },
]

function RouteComponent() {
  const navigate = useNavigate({from: Route.fullPath})
  const {
    page,
    s: search,
    area,
    grade,
    sk: sortKey,
    sd: sortDirection,
  } = Route.useSearch()
  const {offset, limit} = calculateLimitOffsetFromPage(page)
  const {
    data: {
      all_monsters: {total_count, items},
    },
  } = useSuspenseQuery(
    makeQueryOptions(
      offset,
      limit,
      search,
      area,
      grade,
      sortKey,
      sortDirection,
    ),
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs items={monsterBreadcrumbItems} />
        <PageTitle title="Monsters" />
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
                <Section>
                  <Label htmlFor="actor-grade">Type</Label>
                  <Combobox
                    nullable
                    id="actor-type"
                    triggerClassName="col-span-2"
                    value={grade}
                    options={gradeFilterOptions}
                    onValueChange={(value) => {
                      navigate({
                        search: (prev) => ({
                          ...prev,
                          page: 1,
                          grade: value,
                        }),
                      })
                    }}
                  />
                </Section>
              </>
            )}
          </FilterMenu>
        </Filter>

        <GridItemsList items={items}>
          {(items) =>
            items.map((monster) => (
              <GridItem.Item
                key={monster.code}
                from={Route.fullPath}
                to="$code"
                params={{code: monster.code}}
              >
                <GridItem.Icon
                  iconName={monster.icon}
                  actorGrade={monster.grade}
                />
                <GridItem.Details>
                  <GridItem.Name>{monster.name}</GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${monster.level}`,
                      monsterGradeToString(monster.grade),
                      monster.is_sea ? "Sea" : "Land",
                    ]}
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
