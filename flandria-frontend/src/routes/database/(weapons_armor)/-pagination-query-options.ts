import {gqlClient} from "@/lib/graphql-client"

import {Exact, InputMaybe, Scalars} from "@/gql/graphql"

import {searchValidator} from "./-pagination-search-validator"

import {TypedDocumentNode} from "@graphql-typed-document-node/core"
import {queryOptions} from "@tanstack/react-query"

type QueryParams<QueryType, FilterType, SortType> = {
  queryKeyPrefix: string
  query: TypedDocumentNode<
    QueryType,
    Exact<{
      offset: Scalars["Int"]["input"]
      limit: Scalars["Int"]["input"]
      filter?: InputMaybe<FilterType>
      order_by?: InputMaybe<Array<SortType> | SortType>
    }>
  >
}

const buildFilter = <FilterType>(
  searchString: string,
  characterClass: typeof searchValidator.types.output.cc,
  grade: typeof searchValidator.types.output.grade,
  effects: typeof searchValidator.types.output.effects,
): FilterType => {
  const filter = {
    ...(searchString ? {name: {ilike: `%${searchString}%`}} : {}),
    ...(effects.length > 0 ? {effects: {effect_code: {in: effects}}} : {}),
    ...(characterClass === null ? {} : {[characterClass]: {eq: true}}),
    ...(grade === null ? {} : {grade: {eq: grade}}),
  }

  return filter as FilterType
}

export const makeQueryOptionsFactory =
  <QueryType, FilterType, SortType>({
    queryKeyPrefix,
    query,
  }: QueryParams<QueryType, FilterType, SortType>) =>
  (
    offset: number,
    limit: number,
    searchString: string,
    sortKey: typeof searchValidator.types.output.sk,
    sortDirection: typeof searchValidator.types.output.sd,
    characterClass: typeof searchValidator.types.output.cc,
    grade: typeof searchValidator.types.output.grade,
    effects: typeof searchValidator.types.output.effects,
  ) => {
    const filter = buildFilter<FilterType>(
      searchString,
      characterClass,
      grade,
      effects,
    )

    return queryOptions({
      queryKey: [
        queryKeyPrefix,
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
          offset,
          limit,
          filter,
          order_by: [{[sortKey]: sortDirection} as unknown as SortType],
        }),
    })
  }
