import {SortDirection} from "@/gql/graphql"

import {fallback} from "@tanstack/router-zod-adapter"
import z from "zod"

export const sortDirectionValidator = z.nativeEnum(SortDirection)

export const sortDirectionValidatorWithAscDefault = fallback(
  sortDirectionValidator,
  SortDirection.Asc,
).default(SortDirection.Asc)

export const sortDirectionValidatorWithDescDefault = fallback(
  sortDirectionValidator,
  SortDirection.Desc,
).default(SortDirection.Desc)
