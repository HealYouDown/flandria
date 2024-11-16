import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {nameWithDuration} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {AvailableFromQuestCards} from "@/components/detailed-cards/available-from-quest-card"
import {AvailableInRandomboxCard} from "@/components/detailed-cards/available-in-randombox-card"
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

import {shipFlagBreadcrumbItems} from "@/routes/database/(ship)/(routes)/ship_flag"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const shipFlagDetailedDocument = graphql(`
  query ShipFlagDetailed($code: String!) {
    ship_flag(code: $code) {
      ...ItemBase
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

    available_as_quest_reward(code: $code) {
      ...QuestsList_Fragment
    }
  }
`)

const makeQueryOptions = (code: string) =>
  queryOptions({
    queryKey: ["shipFlag", code],
    queryFn: async () => gqlClient.request(shipFlagDetailedDocument, {code}),
  })

export const Route = createFileRoute(
  "/database/(ship)/(routes)/ship_flag/$code",
)({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.ship_flag) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      ship_flag,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!ship_flag) throw notFound()

  const details = useMemo(
    () => [...getBaseMixinDetails(ship_flag)],
    [ship_flag],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...shipFlagBreadcrumbItems,
            {label: ship_flag.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={ship_flag.icon}
              itemGrade={ship_flag.grade}
            />
          }
          title={nameWithDuration(ship_flag.name, ship_flag.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div className="lg:col-span-2">
          <ProducedByCard producers={produced_by} />
          <NeededForCard consumers={needed_for} />
          <SoldByNPCCard npcs={sold_by_npc} />
          <AvailableInRandomboxCard boxes={available_in_randombox} />
          <AvailableFromQuestCards quests={available_as_quest_reward} />
          <DroppedByCard droppedBy={dropped_by} />
        </div>
      </ColsWrapper>
    </>
  )
}
