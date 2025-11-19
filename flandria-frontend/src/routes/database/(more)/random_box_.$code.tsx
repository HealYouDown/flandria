import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"
import {formatPercent} from "@/lib/utils"

import {nameWithDuration} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {AvailableFromQuestCards} from "@/components/detailed-cards/available-from-quest-card"
import {AvailableInRandomboxCard} from "@/components/detailed-cards/available-in-randombox-card"
import {DetailsCard} from "@/components/detailed-cards/details-card"
import {DroppedByCard} from "@/components/detailed-cards/dropped-by-card"
import {GenericItemlistCard} from "@/components/detailed-cards/generic-itemlist-card"
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

import {randomBoxBreadcrumbItems} from "@/routes/database/(more)/random_box"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const randomBoxDetailedDocument = graphql(`
  query RandomBoxDetailed($code: String!) {
    random_box(code: $code) {
      ...ItemBase
      rewards {
        quantity
        probability
        item {
          ...Card_ItemlistItem
        }
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
    queryKey: ["randomBox", code],
    queryFn: async () => gqlClient.request(randomBoxDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(more)/random_box/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.random_box) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      random_box,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!random_box) throw notFound()

  const details = useMemo(
    () => [...getBaseMixinDetails(random_box)],
    [random_box],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...randomBoxBreadcrumbItems,
            {label: random_box.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={random_box.icon}
              itemGrade={random_box.grade}
            />
          }
          title={nameWithDuration(random_box.name, random_box.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div>
          <ProducedByCard producers={produced_by} />
          <NeededForCard consumers={needed_for} />
          <SoldByNPCCard npcs={sold_by_npc} />
          <AvailableInRandomboxCard boxes={available_in_randombox} />
          <AvailableFromQuestCards quests={available_as_quest_reward} />
          <DroppedByCard droppedBy={dropped_by} />
        </div>
        <div>
          <GenericItemlistCard
            title="Content"
            items={random_box.rewards}
            itemlistGetter={(o) => o.item}
            additionalSubsMaker={(o) => {
              const subs = [`Chance: ${formatPercent(o.probability)}`]
              if (o.item.tablename === "money") {
                subs.push(o.quantity.toLocaleString())
              } else if (o.quantity > 1) {
                subs.push(`Qty. ${o.quantity}x`)
              }
              return subs
            }}
          />
        </div>
      </ColsWrapper>
    </>
  )
}
