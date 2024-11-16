import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {nameWithDuration, productionTypeToString} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {Detail, DetailsCard} from "@/components/detailed-cards/details-card"
import {GenericItemlistCard} from "@/components/detailed-cards/generic-itemlist-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {productionBreadcrumbItems} from "@/routes/database/(crafting)/production"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const productionDetailedDocument = graphql(`
  query ProductionDetailed($code: String!) {
    production(code: $code) {
      points_required
      type

      result_quantity
      result_item {
        ...Card_ItemlistItem
      }

      required_materials {
        quantity
        item {
          ...Card_ItemlistItem
        }
      }
    }
  }
`)

const makeQueryOptions = (code: string) =>
  queryOptions({
    queryKey: ["production", code],
    queryFn: async () => gqlClient.request(productionDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(crafting)/production/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.production) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {production},
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!production) throw notFound()

  const details = useMemo<Detail[]>(
    () => [
      {
        label: "2nd Job Type",
        value: productionTypeToString(production.type),
        description: "The type of 2nd Job that can produce the item.",
      },
      {
        label: "Proficiency needed",
        value: production.points_required.toLocaleString(),
        description:
          "How much progress in the 2nd job is needed to craft the item.",
      },
    ],
    [production],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...productionBreadcrumbItems,
            {label: production.result_item.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={production.result_item.icon}
              itemGrade={production.result_item.grade}
            />
          }
          title={nameWithDuration(
            production.result_item.name,
            production.result_item.duration,
          )}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div className="lg:col-span-2">
          <GenericItemlistCard
            title="Result"
            items={[production.result_item]}
            itemlistGetter={(o) => o}
            additionalSubs={
              production.result_quantity > 1
                ? [`Qty. ${production.result_quantity}x`]
                : []
            }
          />
          <GenericItemlistCard
            title="Materials"
            items={production.required_materials}
            itemlistGetter={(o) => o.item}
            additionalSubsMaker={(o) => [`Qty. ${o.quantity}x`]}
          />
        </div>
      </ColsWrapper>
    </>
  )
}
