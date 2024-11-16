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

import {dualsBreadcrumbItems} from "@/routes/database/(weapons_armor)/(weapons)/duals"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const dualsDetailedDocument = graphql(`
  query DualsDetailed($code: String!) {
    duals(code: $code) {
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
    queryKey: ["duals", code],
    queryFn: async () => gqlClient.request(dualsDetailedDocument, {code}),
  })

export const Route = createFileRoute(
  "/database/(weapons_armor)/(weapons)/duals/$code",
)({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.duals) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      duals,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!duals) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Class",
        value: characterClassStringFromObject(duals) ?? "No Class",
      },
      {
        label: "Level",
        value: `${duals.level_land}/${duals.level_sea}`,
      },
      ...getBaseMixinDetails(duals),
    ],
    [duals],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...dualsBreadcrumbItems,
            {label: duals.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={duals.icon}
              itemGrade={duals.grade}
            />
          }
          title={nameWithDuration(duals.name, duals.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          {duals.models && <ModelCard models={duals.models} />}
          <DetailsCard details={details} />
        </div>
        <div>
          <WeaponUpgradeCard
            upgradeRules={duals.upgrade_rule}
            baseMinPhDamage={duals.minimum_physical_damage}
            baseMaxPhDamage={duals.maximum_physical_damage}
            baseMinMagicDamage={duals.minimum_magical_damage}
            baseMaxMagicDamage={duals.maximum_magical_damage}
            baseAttackRange={duals.attack_range}
            baseAttackSpeed={duals.attack_speed}
          />
          <EffectsCard effects={duals.effects} />
          <ItemSetCard itemSet={duals.item_set} />
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
