import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {nameWithDuration, shipClassFromObject} from "@/utils/format-helpers"

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
import {ShipDetailsCard} from "@/components/detailed-cards/ship-details-card"
import {SoldByNPCCard} from "@/components/detailed-cards/sold-by-npc-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {shipSpecialWeaponBreadcrumbItems} from "@/routes/database/(ship)/(routes)/ship_special_weapon"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const shipSpecialWeaponDetailedDocument = graphql(`
  query ShipSpecialWeaponDetailed($code: String!) {
    ship_special_weapon(code: $code) {
      ...ItemBase
      level_sea

      ...ShipDetails
      ...ShipClassFragment
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
    queryKey: ["shipSpecialWeapon", code],
    queryFn: async () =>
      gqlClient.request(shipSpecialWeaponDetailedDocument, {code}),
  })

export const Route = createFileRoute(
  "/database/(ship)/(routes)/ship_special_weapon/$code",
)({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.ship_special_weapon) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      ship_special_weapon,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!ship_special_weapon) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Ship Class",
        value: shipClassFromObject(ship_special_weapon) ?? "No Class",
      },
      {
        label: "Level Sea",
        value: ship_special_weapon.level_sea.toLocaleString(),
      },
      ...getBaseMixinDetails(ship_special_weapon),
    ],
    [ship_special_weapon],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...shipSpecialWeaponBreadcrumbItems,
            {label: ship_special_weapon.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={ship_special_weapon.icon}
              itemGrade={ship_special_weapon.grade}
            />
          }
          title={nameWithDuration(
            ship_special_weapon.name,
            ship_special_weapon.duration,
          )}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div>
          <ShipDetailsCard item={ship_special_weapon} />
          <EffectsCard effects={ship_special_weapon.effects} />
        </div>
        <div>
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
