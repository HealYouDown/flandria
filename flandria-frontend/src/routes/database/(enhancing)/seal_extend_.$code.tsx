import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

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

import {sealExtendBreadcrumbItems} from "@/routes/database/(enhancing)/seal_extend"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const sealExtendDetailedDocument = graphql(`
  query SealExtendDetailed($code: String!) {
    seal_extend: seal_extend_item(code: $code) {
      ...ItemBase
      description
      for_armor
      for_weapons
      for_accessories
      min_item_level
      max_item_level
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
    queryKey: ["sealExtend", code],
    queryFn: async () => gqlClient.request(sealExtendDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(enhancing)/seal_extend/$code")(
  {
    loader: ({params: {code}}) =>
      queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
        if (!resp.seal_extend) throw notFound()
      }),
    component: RouteComponent,
  },
)

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      seal_extend,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!seal_extend) throw notFound()

  const details = useMemo(() => {
    const usableOn = [
      seal_extend.for_weapons && "Weapons",
      seal_extend.for_armor && "Armor",
      seal_extend.for_accessories && "Accessories",
    ].filter(Boolean)

    // A max level of 9999 means there is no upper limit
    const itemLevel =
      seal_extend.max_item_level >= 9999
        ? `${seal_extend.min_item_level}+`
        : `${seal_extend.min_item_level} - ${seal_extend.max_item_level}`

    return [
      {label: "Usable on", value: usableOn.join(", ")},
      {label: "Item level", value: itemLevel},
      ...getBaseMixinDetails(seal_extend),
    ]
  }, [seal_extend])

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...sealExtendBreadcrumbItems,
            {label: seal_extend.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={seal_extend.icon}
              itemGrade={seal_extend.grade}
            />
          }
          title={nameWithDuration(seal_extend.name, seal_extend.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div className="lg:col-span-2">
          {seal_extend.description && (
            <DescriptionCard description={seal_extend.description} />
          )}
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
