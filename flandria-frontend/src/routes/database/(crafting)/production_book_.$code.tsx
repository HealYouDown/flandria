import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {nameWithDuration} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {DetailsCard} from "@/components/detailed-cards/details-card"
import {getBaseMixinDetails} from "@/components/detailed-cards/helpers"
import {SoldByNPCCard} from "@/components/detailed-cards/sold-by-npc-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {productionBookBreadcrumbItems} from "@/routes/database/(crafting)/production_book"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const productionBookDetailedDocument = graphql(`
  query ProductionBookDetailed($code: String!) {
    production_book(code: $code) {
      ...ItemBase
    }

    sold_by_npc(code: $code) {
      ...SoldByNPC
    }
  }
`)

const makeQueryOptions = (code: string) =>
  queryOptions({
    queryKey: ["productionBook", code],
    queryFn: async () =>
      gqlClient.request(productionBookDetailedDocument, {code}),
  })

export const Route = createFileRoute(
  "/database/(crafting)/production_book/$code",
)({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.production_book) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {production_book, sold_by_npc},
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!production_book) throw notFound()

  const details = useMemo(
    () => [...getBaseMixinDetails(production_book)],
    [production_book],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...productionBookBreadcrumbItems,
            {label: production_book.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={production_book.icon}
              itemGrade={production_book.grade}
            />
          }
          title={nameWithDuration(
            production_book.name,
            production_book.duration,
          )}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div className="lg:col-span-2">
          <SoldByNPCCard npcs={sold_by_npc} />
        </div>
      </ColsWrapper>
    </>
  )
}
