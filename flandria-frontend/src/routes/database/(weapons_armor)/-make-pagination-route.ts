import {queryClient} from "@/lib/react-query-client"

import {calculateLimitOffsetFromPage} from "@/utils/pagination"

import {makeQueryOptionsFactory} from "./-pagination-query-options"
import {searchValidator} from "./-pagination-search-validator"

import {Route as DatabaseRootRoute} from "@/routes/database/index"
import {RouteComponent, createRoute} from "@tanstack/react-router"

type MakeWeaponsArmorRouteParams<QueryType, FilterType, SortType> = {
  path: string
  component: RouteComponent
  makeQueryOptions: ReturnType<
    typeof makeQueryOptionsFactory<QueryType, FilterType, SortType>
  >
}
export const makeWeaponsArmorRoute = <QueryType, FilterType, SortType>({
  path,
  component,
  makeQueryOptions,
}: MakeWeaponsArmorRouteParams<QueryType, FilterType, SortType>) => {
  return createRoute({
    path,
    getParentRoute: () => DatabaseRootRoute,
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
    component: component,
    validateSearch: searchValidator,
  })
}
