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

import {upgradeHelpBreadcrumbItems} from "@/routes/database/(enhancing)/upgrade_help"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const upgradeHelpDetailedDocument = graphql(`
  query UpgradeHelpDetailed($code: String!) {
    upgrade_help: upgrade_help_item(code: $code) {
      ...ItemBase
      description
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
    queryKey: ["upgradeHelp", code],
    queryFn: async () => gqlClient.request(upgradeHelpDetailedDocument, {code}),
  })

export const Route = createFileRoute(
  "/database/(enhancing)/upgrade_help/$code",
)({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.upgrade_help) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      upgrade_help,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!upgrade_help) throw notFound()

  const details = useMemo(
    () => [...getBaseMixinDetails(upgrade_help)],
    [upgrade_help],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...upgradeHelpBreadcrumbItems,
            {label: upgrade_help.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={upgrade_help.icon}
              itemGrade={upgrade_help.grade}
            />
          }
          title={nameWithDuration(upgrade_help.name, upgrade_help.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div className="lg:col-span-2">
          {upgrade_help.description && (
            <DescriptionCard description={upgrade_help.description} />
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
