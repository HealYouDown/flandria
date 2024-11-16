import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {AvailableFromQuestCards} from "@/components/detailed-cards/available-from-quest-card"
import {AvailableInRandomboxCard} from "@/components/detailed-cards/available-in-randombox-card"
import {DetailsCard} from "@/components/detailed-cards/details-card"
import {DroppedByCard} from "@/components/detailed-cards/dropped-by-card"
import {getBaseMixinDetails} from "@/components/detailed-cards/helpers"
import {NeededForCard} from "@/components/detailed-cards/needed-for-card"
import {ProducedByCard} from "@/components/detailed-cards/produced-by-card"
import {QuestsListCard} from "@/components/detailed-cards/quests-list-card"
import {SoldByNPCCard} from "@/components/detailed-cards/sold-by-npc-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {questScrollBreadcrumbItems} from "@/routes/database/(quests)/quest_scroll"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const questScrollDetailedDocument = graphql(`
  query QuestScrollDetailed($code: String!) {
    quest_scroll(code: $code) {
      ...ItemBase

      quest {
        ...QuestsList_Fragment
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
    queryKey: ["questScroll", code],
    queryFn: async () => gqlClient.request(questScrollDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(quests)/quest_scroll/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.quest_scroll) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      quest_scroll,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!quest_scroll) throw notFound()

  const details = useMemo(
    () => [...getBaseMixinDetails(quest_scroll)],
    [quest_scroll],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...questScrollBreadcrumbItems,
            {label: quest_scroll.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={quest_scroll.icon}
              itemGrade={quest_scroll.grade}
            />
          }
          title={quest_scroll.name}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div>
          <QuestsListCard quests={[quest_scroll.quest]} />
          <SoldByNPCCard npcs={sold_by_npc} />
          <AvailableInRandomboxCard boxes={available_in_randombox} />
          <NeededForCard consumers={needed_for} />
          <ProducedByCard producers={produced_by} />
          <AvailableFromQuestCards quests={available_as_quest_reward} />
        </div>
        <div>
          <DroppedByCard droppedBy={dropped_by} />
        </div>
      </ColsWrapper>
    </>
  )
}
