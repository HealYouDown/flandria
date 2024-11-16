import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {nameWithDuration, shipClassFromObject} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {AvailableFromQuestCards} from "@/components/detailed-cards/available-from-quest-card"
import {AvailableInRandomboxCard} from "@/components/detailed-cards/available-in-randombox-card"
import {DetailsCard} from "@/components/detailed-cards/details-card"
import {DroppedByCard} from "@/components/detailed-cards/dropped-by-card"
import {EffectsCard} from "@/components/detailed-cards/effects-card"
import {getBaseMixinDetails} from "@/components/detailed-cards/helpers"
import {NeededForCard} from "@/components/detailed-cards/needed-for-card"
import {ProducedByCard} from "@/components/detailed-cards/produced-by-card"
import {ShipDetailsCard} from "@/components/detailed-cards/ship-details-card"
import {SoldByNPCCard} from "@/components/detailed-cards/sold-by-npc-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {shipFrontBreadcrumbItems} from "@/routes/database/(ship)/(routes)/ship_front"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const shipFrontDetailedDocument = graphql(`
  query ShipFrontDetailed($code: String!) {
    ship_front(code: $code) {
      ...ItemBase
      level_sea

      ...ShipDetails
      ...ShipClassFragment
      ...EffectsFragment
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
    queryKey: ["shipFront", code],
    queryFn: async () => gqlClient.request(shipFrontDetailedDocument, {code}),
  })

export const Route = createFileRoute(
  "/database/(ship)/(routes)/ship_front/$code",
)({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.ship_front) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      ship_front,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!ship_front) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Ship Class",
        value: shipClassFromObject(ship_front) ?? "No Class",
      },
      {label: "Level Sea", value: ship_front.level_sea.toLocaleString()},
      ...getBaseMixinDetails(ship_front),
    ],
    [ship_front],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...shipFrontBreadcrumbItems,
            {label: ship_front.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={ship_front.icon}
              itemGrade={ship_front.grade}
            />
          }
          title={nameWithDuration(ship_front.name, ship_front.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div>
          <ShipDetailsCard item={ship_front} />
          <EffectsCard effects={ship_front.effects} />
        </div>
        <div>
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
