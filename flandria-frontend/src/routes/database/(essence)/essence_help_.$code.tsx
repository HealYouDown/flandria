import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {nameWithDuration} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {AvailableInRandomboxCard} from "@/components/detailed-cards/available-in-randombox-card"
import {DescriptionCard} from "@/components/detailed-cards/description-card"
import {DetailsCard} from "@/components/detailed-cards/details-card"
import {DroppedByCard} from "@/components/detailed-cards/dropped-by-card"
import {getBaseMixinDetails} from "@/components/detailed-cards/helpers"
import {NeededForCard} from "@/components/detailed-cards/needed-for-card"
import {ProducedByCard} from "@/components/detailed-cards/produced-by-card"
import {SoldByNPCCard} from "@/components/detailed-cards/sold-by-npc-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {essenceHelpBreadcrumbItems} from "@/routes/database/(essence)/essence_help"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const essenceHelpDetailedDocument = graphql(`
  query EssenceHelpDetailed($code: String!) {
    essence_help: essence_help_item(code: $code) {
      ...ItemBase
      description
    }

    dropped_by(code: $code) {
      ...DroppedBy
    }

    available_in_randombox(code: $code) {
      ...RandomBox
    }

    produced_by(code: $code) {
      ...ProducedBy
    }

    needed_for(code: $code) {
      ...NeededFor
    }

    sold_by_npc(code: $code) {
      ...SoldByNPC
    }
  }
`)

const makeQueryOptions = (code: string) =>
  queryOptions({
    queryKey: ["essenceHelp", code],
    queryFn: async () => gqlClient.request(essenceHelpDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(essence)/essence_help/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.essence_help) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      essence_help,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!essence_help) throw notFound()

  const details = useMemo(
    () => [...getBaseMixinDetails(essence_help)],
    [essence_help],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...essenceHelpBreadcrumbItems,
            {label: essence_help.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={essence_help.icon}
              itemGrade={essence_help.grade}
            />
          }
          title={nameWithDuration(essence_help.name, essence_help.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
          {essence_help.description && (
            <DescriptionCard description={essence_help.description} />
          )}
        </div>
        <div className="lg:col-span-2">
          <NeededForCard consumers={needed_for} />
          <ProducedByCard producers={produced_by} />
          <AvailableInRandomboxCard boxes={available_in_randombox} />
          <SoldByNPCCard npcs={sold_by_npc} />
          <DroppedByCard droppedBy={dropped_by} />
        </div>
      </ColsWrapper>
    </>
  )
}
