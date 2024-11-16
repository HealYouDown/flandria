import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

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

import {recipeBreadcrumbItems} from "@/routes/database/(crafting)/recipe"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const recipeDetailedDocument = graphql(`
  query RecipeDetailed($code: String!) {
    recipe(code: $code) {
      ...ItemBase

      result_quantity
      result_item {
        ...Card_ItemlistItem
      }

      required_materials {
        quantity
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
    queryKey: ["recipe", code],
    queryFn: async () => gqlClient.request(recipeDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(crafting)/recipe/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.recipe) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      recipe,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
      sold_by_npc,
      available_as_quest_reward,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!recipe) throw notFound()

  const details = useMemo(() => [...getBaseMixinDetails(recipe)], [recipe])

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...recipeBreadcrumbItems,
            {label: recipe.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={recipe.icon}
              itemGrade={recipe.grade}
            />
          }
          title={nameWithDuration(recipe.name, recipe.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div>
          <GenericItemlistCard
            title="Result"
            items={[recipe.result_item]}
            itemlistGetter={(o) => o}
            additionalSubs={
              recipe.result_quantity > 1
                ? [`Qty. ${recipe.result_quantity}x`]
                : []
            }
          />
          <GenericItemlistCard
            title="Materials"
            items={recipe.required_materials}
            itemlistGetter={(o) => o.item}
            additionalSubsMaker={(o) => [`Qty. ${o.quantity}x`]}
          />
        </div>
        <div>
          <NeededForCard consumers={needed_for} />
          <ProducedByCard producers={produced_by} />
          <SoldByNPCCard npcs={sold_by_npc} />
          <DroppedByCard droppedBy={dropped_by} />
          <AvailableInRandomboxCard boxes={available_in_randombox} />
          <AvailableFromQuestCards quests={available_as_quest_reward} />
        </div>
      </ColsWrapper>
    </>
  )
}
