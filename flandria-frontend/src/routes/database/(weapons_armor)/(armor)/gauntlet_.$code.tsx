import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {
  characterClassStringFromObject,
  nameWithDuration,
} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {ArmorUpgradeCard} from "@/components/detailed-cards/armor-upgrade-card"
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
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {gauntletBreadcrumbItems} from "@/routes/database/(weapons_armor)/(armor)/gauntlet"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const gauntletDetailedDocument = graphql(`
  query GauntletDetailed($code: String!) {
    gauntlet: gauntlets(code: $code) {
      ...ItemBase

      level_land
      level_sea

      ...ItemSetCard
      ...CharacterClassFragment
      ...EffectsFragment

      physical_defense
      magical_defense
      upgrade_rule {
        ...UpgradeRule
      }

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
    queryKey: ["gauntlet", code],
    queryFn: async () => gqlClient.request(gauntletDetailedDocument, {code}),
  })

export const Route = createFileRoute(
  "/database/(weapons_armor)/(armor)/gauntlet/$code",
)({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.gauntlet) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      gauntlet,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!gauntlet) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Class",
        value: characterClassStringFromObject(gauntlet) ?? "No Class",
      },
      {
        label: "Level",
        value: `${gauntlet.level_land}/${gauntlet.level_sea}`,
      },
      ...getBaseMixinDetails(gauntlet),
    ],
    [gauntlet],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...gauntletBreadcrumbItems,
            {label: gauntlet.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={gauntlet.icon}
              itemGrade={gauntlet.grade}
            />
          }
          title={nameWithDuration(gauntlet.name, gauntlet.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          {gauntlet.models && <ModelCard models={gauntlet.models} />}
          <DetailsCard details={details} />
        </div>
        <div>
          <ArmorUpgradeCard
            upgradeRules={gauntlet.upgrade_rule}
            basePhysicalDefense={gauntlet.physical_defense}
            baseMagicalDefense={gauntlet.magical_defense}
            baseAttackSpeed={0}
            baseHitrate={0}
          />
          <EffectsCard effects={gauntlet.effects} />
          <ItemSetCard itemSet={gauntlet.item_set} />
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
