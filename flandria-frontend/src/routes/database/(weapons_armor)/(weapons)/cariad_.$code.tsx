import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {
  characterClassStringFromObject,
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
import {ItemSetCard} from "@/components/detailed-cards/item-set-card"
import {ModelCard} from "@/components/detailed-cards/model-card"
import {NeededForCard} from "@/components/detailed-cards/needed-for-card"
import {ProducedByCard} from "@/components/detailed-cards/produced-by-card"
import {SoldByNPCCard} from "@/components/detailed-cards/sold-by-npc-card"
import {WeaponUpgradeCard} from "@/components/detailed-cards/weapon-upgrade-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {cariadBreadcrumbItems} from "@/routes/database/(weapons_armor)/(weapons)/cariad"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const cariadDetailedDocument = graphql(`
  query CariadDetailed($code: String!) {
    cariad(code: $code) {
      ...ItemBase

      level_land
      level_sea

      ...ItemSetCard
      ...CharacterClassFragment
      ...WeaponUpgradeRule
      ...EffectsFragment

      minimum_physical_damage
      maximum_physical_damage
      minimum_magical_damage
      maximum_magical_damage
      attack_speed
      attack_range

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
    queryKey: ["cariad", code],
    queryFn: async () => gqlClient.request(cariadDetailedDocument, {code}),
  })

export const Route = createFileRoute(
  "/database/(weapons_armor)/(weapons)/cariad/$code",
)({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.cariad) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      cariad,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!cariad) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Class",
        value: characterClassStringFromObject(cariad) ?? "No Class",
      },
      {
        label: "Level",
        value: `${cariad.level_land}/${cariad.level_sea}`,
      },
      ...getBaseMixinDetails(cariad),
    ],
    [cariad],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...cariadBreadcrumbItems,
            {label: cariad.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={cariad.icon}
              itemGrade={cariad.grade}
            />
          }
          title={nameWithDuration(cariad.name, cariad.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          {cariad.models && <ModelCard models={cariad.models} />}
          <DetailsCard details={details} />
        </div>
        <div>
          <WeaponUpgradeCard
            upgradeRules={cariad.upgrade_rule}
            baseMinPhDamage={cariad.minimum_physical_damage}
            baseMaxPhDamage={cariad.maximum_physical_damage}
            baseMinMagicDamage={cariad.minimum_magical_damage}
            baseMaxMagicDamage={cariad.maximum_magical_damage}
            baseAttackRange={cariad.attack_range}
            baseAttackSpeed={cariad.attack_speed}
          />
          <EffectsCard effects={cariad.effects} />
          <ItemSetCard itemSet={cariad.item_set} />
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
