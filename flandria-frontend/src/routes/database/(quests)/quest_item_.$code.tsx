import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {AvailableFromQuestCards} from "@/components/detailed-cards/available-from-quest-card"
import {DetailsCard} from "@/components/detailed-cards/details-card"
import {DroppedByCard} from "@/components/detailed-cards/dropped-by-card"
import {getBaseMixinDetails} from "@/components/detailed-cards/helpers"
import {QuestsListCard} from "@/components/detailed-cards/quests-list-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {questItemBreadcrumbItems} from "@/routes/database/(quests)/quest_item"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const questItemDetailedDocument = graphql(`
  query QuestItemDetailed($code: String!) {
    quest_item(code: $code) {
      ...ItemBase
    }

    quests_by_give_item: all_quests(
      limit: -1
      filter: {give_items: {item_code: {eq: $code}}}
    ) {
      items {
        ...QuestsList_Fragment
      }
    }

    quests_by_mission: all_quests(
      limit: -1
      filter: {missions: {quest_item_code: {eq: $code}}}
    ) {
      items {
        ...QuestsList_Fragment
      }
    }

    dropped_by(code: $code) {
      ...DroppedBy
    }

    available_as_quest_reward(code: $code) {
      ...QuestsList_Fragment
    }
  }
`)

const makeQueryOptions = (code: string) =>
  queryOptions({
    queryKey: ["questItem", code],
    queryFn: async () => gqlClient.request(questItemDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(quests)/quest_item/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.quest_item) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      quest_item,
      dropped_by,
      available_as_quest_reward,
      quests_by_give_item,
      quests_by_mission,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!quest_item) throw notFound()

  const details = useMemo(
    () => [...getBaseMixinDetails(quest_item)],
    [quest_item],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...questItemBreadcrumbItems,
            {label: quest_item.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={quest_item.icon}
              itemGrade={quest_item.grade}
            />
          }
          title={quest_item.name}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div>
          <QuestsListCard
            quests={[...quests_by_give_item.items, ...quests_by_mission.items]}
          />
        </div>
        <div>
          <AvailableFromQuestCards quests={available_as_quest_reward} />
          <DroppedByCard droppedBy={dropped_by} />
        </div>
      </ColsWrapper>
    </>
  )
}
