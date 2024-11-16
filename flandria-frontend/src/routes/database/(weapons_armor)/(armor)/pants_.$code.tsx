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

import {pantsBreadcrumbItems} from "@/routes/database/(weapons_armor)/(armor)/pants"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const pantsDetailedDocument = graphql(`
  query PantsDetailed($code: String!) {
    pants(code: $code) {
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
    queryKey: ["pants", code],
    queryFn: async () => gqlClient.request(pantsDetailedDocument, {code}),
  })

export const Route = createFileRoute(
  "/database/(weapons_armor)/(armor)/pants/$code",
)({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.pants) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      pants,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!pants) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Class",
        value: characterClassStringFromObject(pants) ?? "No Class",
      },
      {
        label: "Level",
        value: `${pants.level_land}/${pants.level_sea}`,
      },
      ...getBaseMixinDetails(pants),
    ],
    [pants],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...pantsBreadcrumbItems,
            {label: pants.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={pants.icon}
              itemGrade={pants.grade}
            />
          }
          title={nameWithDuration(pants.name, pants.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          {pants.models && <ModelCard models={pants.models} />}
          <DetailsCard details={details} />
        </div>
        <div>
          <ArmorUpgradeCard
            upgradeRules={pants.upgrade_rule}
            basePhysicalDefense={pants.physical_defense}
            baseMagicalDefense={pants.magical_defense}
          />
          <EffectsCard effects={pants.effects} />
          <ItemSetCard itemSet={pants.item_set} />
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
