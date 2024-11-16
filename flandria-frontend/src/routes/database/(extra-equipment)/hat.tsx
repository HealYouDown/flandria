import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {
  characterClassStringFromObject,
  genderToString,
} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {pageValidator} from "@/utils/search-validators/page-validator"
import {searchStringValidator} from "@/utils/search-validators/search-string-validator"
import {sortDirectionValidatorWithDescDefault} from "@/utils/search-validators/sort-direction-validators"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {DressSort, HatSort} from "@/gql/graphql"

import {ComboboxOption} from "@/components/combobox"
import {
  CharacterClassFilterSection,
  characterClassValidators,
} from "@/components/filters/CharacterClassFilterSection"
import {
  EffectsFilterSection,
  effectsValidator,
} from "@/components/filters/EffectsFilterSection"
import {FilterSearchBar} from "@/components/filters/FilterSearchBar"
import {
  ItemGradeFilterSection,
  itemGradeValidator,
} from "@/components/filters/ItemGradeFilterSection"
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
  query HatsPagination(
    $offset: Int!
    $limit: Int!
    $filter: HatFilter
    $order_by: [HatSort!]
  ) {
    all_hats(
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
        level_land
        level_sea
        grade
        duration
        gender
        ...CharacterClassFragment
        ...EffectsFragment
      }
    }
  }
`)

type AllowedSortOptions = keyof HatSort
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
    label: "Level Land",
    value: "level_land",
  },
  {
    label: "Level Sea",
    value: "level_sea",
  },
] as const
const sortKeyValidator = z.custom<AllowedSortOptions>((val) =>
  sortOptions.map((o) => o.value).includes(val),
)

const searchValidator = zodSearchValidator(
  z.object({
    page: pageValidator,
    s: searchStringValidator,
    cc: fallback(characterClassValidators.nullable(), null).default(null),
    grade: fallback(itemGradeValidator.nullable(), null).default(null),
    effects: fallback(effectsValidator, []).default([]),
    sk: fallback(sortKeyValidator, "row_id").default("row_id"),
    sd: sortDirectionValidatorWithDescDefault,
  }),
)

const makeQueryOptions = (
  offset: number,
  limit: number,
  searchString: string,
  sortKey: typeof searchValidator.types.output.sk,
  sortDirection: typeof searchValidator.types.output.sd,
  characterClass: typeof searchValidator.types.output.cc,
  grade: typeof searchValidator.types.output.grade,
  effects: typeof searchValidator.types.output.effects,
) =>
  queryOptions({
    queryKey: [
      "allHats",
      offset,
      limit,
      sortKey,
      sortDirection,
      characterClass,
      effects,
      grade,
      searchString,
    ],
    queryFn: async () =>
      gqlClient.request(query, {
        offset: offset,
        limit: limit,
        filter: {
          ...(searchString ? {name: {ilike: `%${searchString}%`}} : {}),
          ...(effects.length > 0
            ? {effects: {effect_code: {in: effects}}}
            : {}),
          ...(characterClass === null ? {} : {[characterClass]: {eq: true}}),
          ...(grade === null ? {} : {grade: {eq: grade}}),
        },
        order_by: [{[sortKey]: sortDirection} as unknown as DressSort],
      }),
  })

export const Route = createFileRoute("/database/(extra-equipment)/hat")({
  loaderDeps: ({
    search: {
      page,
      s: searchString,
      sk: sortKey,
      sd: sortDirection,
      cc: characterClass,
      grade,
      effects,
    },
  }) => ({
    ...calculateLimitOffsetFromPage(page),
    sortKey,
    sortDirection,
    characterClass,
    grade,
    effects,
    searchString,
  }),
  loader: ({
    deps: {
      offset,
      limit,
      searchString,
      sortKey,
      sortDirection,
      characterClass,
      grade,
      effects,
    },
  }) =>
    queryClient.ensureQueryData(
      makeQueryOptions(
        offset,
        limit,
        searchString,
        sortKey,
        sortDirection,
        characterClass,
        grade,
        effects,
      ),
    ),
  component: RouteComponent,
  validateSearch: searchValidator,
})

export const hatBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Hats",
    href: "/database/hat",
  },
]

function RouteComponent() {
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
      all_hats: {total_count, items},
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
        <PageHeaderBreadcrumbs items={hatBreadcrumbItems} />
        <PageTitle title={last(hatBreadcrumbItems)!.label} />
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
            items.map((hat) => (
              <GridItem.Item
                key={hat.code}
                from={Route.fullPath}
                to="$code"
                params={{code: hat.code}}
              >
                <GridItem.Icon iconName={hat.icon} itemGrade={hat.grade} />
                <GridItem.Details>
                  <GridItem.Name duration={hat.duration}>
                    {hat.name}
                  </GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${hat.level_land}/${hat.level_sea}`,
                      genderToString(hat.gender),
                      characterClassStringFromObject(hat),
                    ]}
                  />
                  <GridItem.Effects effects={hat.effects} />
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
