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
import {ModelCard} from "@/components/detailed-cards/model-card"
import {NeededForCard} from "@/components/detailed-cards/needed-for-card"
import {ProducedByCard} from "@/components/detailed-cards/produced-by-card"
import {SoldByNPCCard} from "@/components/detailed-cards/sold-by-npc-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {hatBreadcrumbItems} from "@/routes/database/(extra-equipment)/hat"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const hatDetailedDocument = graphql(`
  query HatDetailed($code: String!) {
    hat(code: $code) {
      ...ItemBase

      level_land
      level_sea
      gender

      ...CharacterClassFragment
      ...EffectsFragment

      models {
        ...ModelFragment
      }
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
    queryKey: ["hat", code],
    queryFn: async () => gqlClient.request(hatDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(extra-equipment)/hat/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.hat) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      hat,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!hat) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Class",
        value: characterClassStringFromObject(hat) ?? "No Class",
      },
      {
        label: "Gender",
        value: genderToString(hat.gender),
      },
      {
        label: "Level",
        value: `${hat.level_land}/${hat.level_sea}`,
      },
      ...getBaseMixinDetails(hat),
    ],
    [hat],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...hatBreadcrumbItems,
            {label: hat.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={hat.icon}
              itemGrade={hat.grade}
            />
          }
          title={nameWithDuration(hat.name, hat.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          {hat.models && <ModelCard models={hat.models} />}
          <DetailsCard details={details} />
        </div>
        <div>
          <EffectsCard effects={hat.effects} />
        </div>
        <div>
          <AvailableInRandomboxCard boxes={available_in_randombox} />
          <NeededForCard consumers={needed_for} />
          <ProducedByCard producers={produced_by} />
          <AvailableFromQuestCards quests={available_as_quest_reward} />
          <SoldByNPCCard npcs={sold_by_npc} />
          <DroppedByCard droppedBy={dropped_by} />
        </div>
      </ColsWrapper>
    </>
  )
}
