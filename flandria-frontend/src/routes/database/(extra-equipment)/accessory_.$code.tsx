import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {
  characterClassStringFromObject,
  genderToString,
  nameWithDuration,
} from "@/utils/format-helpers"

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
import {SoldByNPCCard} from "@/components/detailed-cards/sold-by-npc-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {accessoryBreadcrumbItems} from "@/routes/database/(extra-equipment)/accessory"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const accessoryDetailedDocument = graphql(`
  query AccessoryDetailed($code: String!) {
    accessory(code: $code) {
      ...ItemBase

      level_land
      level_sea
      gender

      ...CharacterClassFragment
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
    queryKey: ["accessory", code],
    queryFn: async () => gqlClient.request(accessoryDetailedDocument, {code}),
  })

export const Route = createFileRoute(
  "/database/(extra-equipment)/accessory/$code",
)({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.accessory) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      accessory,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!accessory) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Class",
        value: characterClassStringFromObject(accessory) ?? "No Class",
      },
      {
        label: "Gender",
        value: genderToString(accessory.gender),
      },
      {
        label: "Level",
        value: `${accessory.level_land}/${accessory.level_sea}`,
      },
      ...getBaseMixinDetails(accessory),
    ],
    [accessory],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...accessoryBreadcrumbItems,
            {label: accessory.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={accessory.icon}
              itemGrade={accessory.grade}
            />
          }
          title={nameWithDuration(accessory.name, accessory.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div>
          <EffectsCard effects={accessory.effects} />
          <AvailableInRandomboxCard boxes={available_in_randombox} />
          <NeededForCard consumers={needed_for} />
          <ProducedByCard producers={produced_by} />
          <AvailableFromQuestCards quests={available_as_quest_reward} />
        </div>
        <div>
          <DroppedByCard droppedBy={dropped_by} />
          <SoldByNPCCard npcs={sold_by_npc} />
        </div>
      </ColsWrapper>
    </>
  )
}
