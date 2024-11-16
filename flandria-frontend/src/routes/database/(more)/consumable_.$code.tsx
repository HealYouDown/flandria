import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {formatSeconds} from "@/utils/date-helpers"
import {nameWithDuration} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {AvailableFromQuestCards} from "@/components/detailed-cards/available-from-quest-card"
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

import {consumableBreadcrumbItems} from "@/routes/database/(more)/consumable"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const consumableDetailedDocument = graphql(`
  query ConsumableDetailed($code: String!) {
    consumable(code: $code) {
      description
      level_land
      level_sea
      cooldown
      cooldown_id
      cast_time
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
    queryKey: ["consumable", code],
    queryFn: async () => gqlClient.request(consumableDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(more)/consumable/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.consumable) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      consumable,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!consumable) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Level",
        value: `${consumable.level_land}/${consumable.level_sea}`,
      },
      {
        label: "Cooldown",
        value: formatSeconds(consumable.cooldown),
      },
      {
        label: "Cast Time",
        value:
          consumable.cast_time === 0
            ? "Instant"
            : formatSeconds(consumable.cast_time),
      },
      {
        label: "Cooldown ID",
        value: consumable.cooldown_id.toString(),
        description: "Items with the same ID share their cooldown.",
      },
      ...getBaseMixinDetails(consumable),
    ],
    [consumable],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...consumableBreadcrumbItems,
            {label: consumable.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={consumable.icon}
              itemGrade={consumable.grade}
            />
          }
          title={nameWithDuration(consumable.name, consumable.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        {consumable.description && (
          <div>
            <DescriptionCard description={consumable.description} />
          </div>
        )}
        <div className={!consumable.description ? "lg:col-span-2" : undefined}>
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
