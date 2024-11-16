import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {characterClassStringFromObject} from "@/utils/format-helpers"
import {calculateLimitOffsetFromPage} from "@/utils/pagination"
import {pageValidator} from "@/utils/search-validators/page-validator"
import {searchStringValidator} from "@/utils/search-validators/search-string-validator"
import {sortDirectionValidatorWithDescDefault} from "@/utils/search-validators/sort-direction-validators"
import {last} from "@/utils/utils"

import {graphql} from "@/gql"
import {QuestSort} from "@/gql/graphql"

import {ComboboxOption} from "@/components/combobox"
import {
  CharacterClassFilterSection,
  characterClassValidators,
} from "@/components/filters/CharacterClassFilterSection"
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
  query QuestsPagination(
    $offset: Int!
    $limit: Int!
    $filter: QuestFilter
    $order_by: [QuestSort!]
  ) {
    all_quests(
      offset: $offset
      limit: $limit
      filter: $filter
      order_by: $order_by
    ) {
      total_count
      items {
        code
        title
        level
        is_sea
        is_explorer
        is_mercenary
        is_noble
        is_saint
        start_area {
          name
        }
      }
    }
  }
`)

type AllowedSortOptions = keyof QuestSort
const sortOptions: ComboboxOption<AllowedSortOptions>[] = [
  {
    label: "Name",
    value: "title",
  },
  {
    label: "Level",
    value: "level",
  },
] as const
const sortKeyValidator = z.custom<AllowedSortOptions>((val) =>
  sortOptions.map((o) => o.value).includes(val),
)

const searchValidator = zodSearchValidator(
  z.object({
    page: pageValidator,
    s: searchStringValidator,
    area: fallback(landSeaValidator.nullable(), null).default(null),
    cc: fallback(characterClassValidators.nullable(), null).default(null),
    sk: fallback(sortKeyValidator, "level").default("level"),
    sd: sortDirectionValidatorWithDescDefault,
  }),
)

const makeQueryOptions = (
  offset: number,
  limit: number,
  searchString: string,
  area: typeof searchValidator.types.output.area,
  sortKey: typeof searchValidator.types.output.sk,
  sortDirection: typeof searchValidator.types.output.sd,
  characterClass: typeof searchValidator.types.output.cc,
) =>
  queryOptions({
    queryKey: [
      "allQuests",
      offset,
      limit,
      area,
      sortKey,
      sortDirection,
      characterClass,
      searchString,
    ],
    queryFn: async () =>
      gqlClient.request(query, {
        offset: offset,
        limit: limit,
        filter: {
          ...(searchString ? {title: {ilike: `%${searchString}%`}} : {}),
          ...(area !== null ? {is_sea: {eq: area === "sea"}} : {}),
          ...(characterClass === null ? {} : {[characterClass]: {eq: true}}),
        },
        order_by: [{[sortKey]: sortDirection} as unknown as QuestSort],
      }),
  })

export const Route = createFileRoute("/database/(quests)/quest")({
  loaderDeps: ({
    search: {
      page,
      s: searchString,
      area,
      sk: sortKey,
      sd: sortDirection,
      cc: characterClass,
    },
  }) => ({
    ...calculateLimitOffsetFromPage(page),
    area,
    sortKey,
    sortDirection,
    characterClass,
    searchString,
  }),
  loader: ({
    deps: {
      offset,
      limit,
      searchString,
      area,
      sortKey,
      sortDirection,
      characterClass,
    },
  }) =>
    queryClient.ensureQueryData(
      makeQueryOptions(
        offset,
        limit,
        searchString,
        area,
        sortKey,
        sortDirection,
        characterClass,
      ),
    ),
  component: RouteComponent,
  validateSearch: searchValidator,
})

export const questBreadcrumbItems: BreadcrumbItem[] = [
  ...databaseBreadcrumbItems,
  {
    label: "Quests",
    href: "/database/quest",
  },
]

function RouteComponent() {
  const navigate = useNavigate({from: Route.fullPath})
  const {
    page,
    s: search,
    area,
    sk: sortKey,
    sd: sortDirection,
    cc: characterClass,
  } = Route.useSearch()
  const {offset, limit} = calculateLimitOffsetFromPage(page)
  const {
    data: {
      all_quests: {total_count, items},
    },
  } = useSuspenseQuery(
    makeQueryOptions(
      offset,
      limit,
      search,
      area,
      sortKey,
      sortDirection,
      characterClass,
    ),
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs items={questBreadcrumbItems} />
        <PageTitle title={last(questBreadcrumbItems)!.label} />
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
                <CharacterClassFilterSection
                  basesClassOnly
                  Section={Section}
                  Label={Label}
                  cc={characterClass}
                  navigate={navigate}
                />
              </>
            )}
          </FilterMenu>
        </Filter>
        <GridItemsList items={items}>
          {(items) =>
            items.map((quest) => (
              <GridItem.Item
                key={quest.code}
                from={Route.fullPath}
                to="$code"
                params={{code: quest.code}}
              >
                <GridItem.Details>
                  <GridItem.Name>{quest.title}</GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${quest.level}`,
                      quest.is_sea ? "Sea" : "Land",
                      characterClassStringFromObject(quest),
                      quest.start_area ? quest.start_area.name : null,
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
