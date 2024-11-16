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

import {rifleBreadcrumbItems} from "@/routes/database/(weapons_armor)/(weapons)/rifle"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const rifleDetailedDocument = graphql(`
  query RifleDetailed($code: String!) {
    rifle(code: $code) {
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
    queryKey: ["rifle", code],
    queryFn: async () => gqlClient.request(rifleDetailedDocument, {code}),
  })

export const Route = createFileRoute(
  "/database/(weapons_armor)/(weapons)/rifle/$code",
)({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.rifle) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      rifle,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!rifle) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Class",
        value: characterClassStringFromObject(rifle) ?? "No Class",
      },
      {
        label: "Level",
        value: `${rifle.level_land}/${rifle.level_sea}`,
      },
      ...getBaseMixinDetails(rifle),
    ],
    [rifle],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...rifleBreadcrumbItems,
            {label: rifle.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={rifle.icon}
              itemGrade={rifle.grade}
            />
          }
          title={nameWithDuration(rifle.name, rifle.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          {rifle.models && <ModelCard models={rifle.models} />}
          <DetailsCard details={details} />
        </div>
        <div>
          <WeaponUpgradeCard
            upgradeRules={rifle.upgrade_rule}
            baseMinPhDamage={rifle.minimum_physical_damage}
            baseMaxPhDamage={rifle.maximum_physical_damage}
            baseMinMagicDamage={rifle.minimum_magical_damage}
            baseMaxMagicDamage={rifle.maximum_magical_damage}
            baseAttackRange={rifle.attack_range}
            baseAttackSpeed={rifle.attack_speed}
          />
          <EffectsCard effects={rifle.effects} />
          <ItemSetCard itemSet={rifle.item_set} />
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
