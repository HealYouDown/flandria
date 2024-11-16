import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {characterClassStringFromObject} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {DescriptionCard} from "@/components/detailed-cards/description-card"
import {Detail, DetailsCard} from "@/components/detailed-cards/details-card"
import {QuestMissionsCard} from "@/components/detailed-cards/quest-missions-card"
import {QuestRewardsCard} from "@/components/detailed-cards/quest-rewards-card"
import {QuestsListCard} from "@/components/detailed-cards/quests-list-card"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {questBreadcrumbItems} from "@/routes/database/(quests)/quest"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {Link, createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const questDetailedDocument = graphql(`
  query QuestDetailed($code: String!) {
    quest(code: $code) {
      code
      title
      is_sea
      level
      is_noble
      is_saint
      is_mercenary
      is_explorer

      start_area {
        map_code
        name
      }
      start_npc {
        code
        name
      }
      end_npc {
        code
        name
      }

      money
      experience

      description
      pre_dialog
      start_dialog
      run_dialog
      finish_dialog

      previous_quest {
        ...QuestsList_Fragment
      }

      selectable_items_count
      reward_items {
        ...QuestRewardEdge
      }

      ...QuestMissions
    }

    next_quests: all_quests(filter: {previous_quest_code: {eq: $code}}) {
      items {
        ...QuestsList_Fragment
      }
    }
  }
`)

const makeQueryOptions = (code: string) =>
  queryOptions({
    queryKey: ["quest", code],
    queryFn: async () => gqlClient.request(questDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(quests)/quest/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.quest) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {quest, next_quests},
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!quest) throw notFound()

  const details = useMemo<Detail[]>(() => {
    const details: Detail[] = [
      {
        label: "Class",
        value: characterClassStringFromObject(quest) ?? "No Class",
      },
      {
        label: "Level",
        value: quest.level.toString(),
      },
      {
        label: "Type",
        value: quest.is_sea ? "Sea" : "Land",
      },
      {
        label: "Experience",
        value: quest.experience.toLocaleString(),
      },
      {
        label: "Reward Money",
        value: quest.money.toLocaleString(),
      },
    ]

    if (quest.start_area) {
      details.push({
        label: "Start Area",
        value: (
          <Link
            to="/database/map/$code"
            params={{code: quest.start_area.map_code}}
          >
            {quest.start_area.name}
          </Link>
        ),
      })
    }

    if (quest.start_npc) {
      details.push({
        label: "Start NPC",
        value: (
          <Link to="/database/npc/$code" params={{code: quest.start_npc.code}}>
            {quest.start_npc.name}
          </Link>
        ),
      })
    }

    if (quest.end_npc) {
      details.push({
        label: "End NPC",
        value: (
          <Link to="/database/npc/$code" params={{code: quest.end_npc.code}}>
            {quest.end_npc.name}
          </Link>
        ),
      })
    }

    return details
  }, [quest])

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...questBreadcrumbItems,
            {label: quest.title, href: Route.fullPath},
          ]}
        />
        <PageTitle title={quest.title} />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
          {quest.previous_quest && (
            <QuestsListCard
              title="Previous Quest"
              quests={[quest.previous_quest]}
            />
          )}
          <QuestsListCard
            title="Next Quest"
            quests={next_quests.items}
            renderIfEmpty={false}
          />
        </div>
        <div>
          <QuestMissionsCard
            missions={quest.missions}
            giveItems={quest.give_items}
          />
          <QuestRewardsCard
            rewards={quest.reward_items}
            selectableCount={quest.selectable_items_count}
          />
        </div>
        <div>
          {quest.description && (
            <DescriptionCard
              title="Description"
              description={quest.description}
            />
          )}
          {quest.pre_dialog && (
            <DescriptionCard
              title="Preview Dialog"
              description={quest.pre_dialog}
            />
          )}
          {quest.start_dialog && (
            <DescriptionCard
              title="Start Dialog"
              description={quest.start_dialog}
            />
          )}
          {quest.run_dialog && (
            <DescriptionCard
              title="Run Dialog"
              description={quest.run_dialog}
            />
          )}
          {quest.finish_dialog && (
            <DescriptionCard
              title="Finish Dialog"
              description={quest.finish_dialog}
            />
          )}
        </div>
      </ColsWrapper>
    </>
  )
}
