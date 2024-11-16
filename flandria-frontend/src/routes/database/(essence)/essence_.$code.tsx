import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {
  essenceEquipTypeToString,
  nameWithDuration,
} from "@/utils/format-helpers"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {AvailableInRandomboxCard} from "@/components/detailed-cards/available-in-randombox-card"
import {DetailsCard} from "@/components/detailed-cards/details-card"
import {DroppedByCard} from "@/components/detailed-cards/dropped-by-card"
import {EffectsCard} from "@/components/detailed-cards/effects-card"
import {getBaseMixinDetails} from "@/components/detailed-cards/helpers"
import {NeededForCard} from "@/components/detailed-cards/needed-for-card"
import {ProducedByCard} from "@/components/detailed-cards/produced-by-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {essenceBreadcrumbItems} from "@/routes/database/(essence)/essence"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const essenceDetailedDocument = graphql(`
  query EssenceDetailed($code: String!) {
    essence(code: $code) {
      ...ItemBase

      required_level
      is_core
      equip_type

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
  }
`)

const makeQueryOptions = (code: string) =>
  queryOptions({
    queryKey: ["essence", code],
    queryFn: async () => gqlClient.request(essenceDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(essence)/essence/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.essence) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {
      essence,
      dropped_by,
      available_in_randombox,
      produced_by,
      needed_for,
    },
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!essence) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Type",
        value: essenceEquipTypeToString(essence.equip_type),
        description: "The item type that accepts the essence.",
      },
      {
        label: "Slot",
        value: essence.is_core ? "Core" : "Meta",
        description: "Core essences require a golden slot on your item.",
      },
      {
        label: "Required Item Level",
        value: `${essence.required_level}`,
        description: "The minimum required level of the item.",
      },
      ...getBaseMixinDetails(essence),
    ],
    [essence],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...essenceBreadcrumbItems,
            {label: essence.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={essence.icon}
              itemGrade={essence.grade}
            />
          }
          title={nameWithDuration(essence.name, essence.duration)}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          <DetailsCard details={details} />
        </div>
        <div>
          <EffectsCard effects={essence.effects} />
          <NeededForCard consumers={needed_for} />
          <ProducedByCard producers={produced_by} />
        </div>
        <div>
          <AvailableInRandomboxCard boxes={available_in_randombox} />
          <DroppedByCard droppedBy={dropped_by} />
        </div>
      </ColsWrapper>
    </>
  )
}
