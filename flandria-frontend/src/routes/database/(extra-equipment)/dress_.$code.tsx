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

import {dressBreadcrumbItems} from "@/routes/database/(extra-equipment)/dress"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const dressDetailedDocument = graphql(`
  query DressDetailed($code: String!) {
    dress(code: $code) {
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
    queryKey: ["dress", code],
    queryFn: async () => gqlClient.request(dressDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(extra-equipment)/dress/$code")(
  {
    loader: ({params: {code}}) =>
      queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
        if (!resp.dress) throw notFound()
      }),
    component: RouteComponent,
  },
)

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      dress,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!dress) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Class",
        value: characterClassStringFromObject(dress) ?? "No Class",
      },
      {
        label: "Gender",
        value: genderToString(dress.gender),
      },
      {
        label: "Level",
        value: `${dress.level_land}/${dress.level_sea}`,
      },
      ...getBaseMixinDetails(dress),
    ],
    [dress],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...dressBreadcrumbItems,
            {label: dress.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={dress.icon}
              itemGrade={dress.grade}
            />
          }
          title={nameWithDuration(dress.name, dress.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          {dress.models && <ModelCard models={dress.models} />}
          <DetailsCard details={details} />
        </div>
        <div>
          <EffectsCard effects={dress.effects} />
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
