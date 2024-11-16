import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {graphql} from "@/gql"

import {ColsWrapper} from "@/components/cols-wrapper"
import {DetailsCard} from "@/components/detailed-cards/details-card"
import {MapCard} from "@/components/detailed-cards/map-card"
import {ModelCard} from "@/components/detailed-cards/model-card"
import {NPCStoreCard} from "@/components/detailed-cards/npc-store-card"
import {QuestsListCard} from "@/components/detailed-cards/quests-list-card"
import {ItemIcon} from "@/components/grid-item/ItemIcon"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"

import {npcBreadcrumbItems} from "@/routes/database/(actors)/npc"
import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import {useMemo} from "react"

const npcDetailedDocument = graphql(`
  query NPCDetailed($code: String!) {
    npc(code: $code) {
      code
      name
      icon
      grade
      is_sea
      level
      health_points

      models {
        ...ModelFragment
      }

      positions {
        map_code
        ...MapCanvas_NPCPositionFragment
      }

      store_items {
        ...NPCStoreItemlist_Fragment
      }
    }

    # less data queried instead of asking for map data on each positions edge
    maps: all_maps(limit: -1, filter: {npcs: {npc_code: {eq: $code}}}) {
      items {
        ...MapCanvas_MapDetailsFragment
      }
    }

    quests: all_quests(limit: -1, filter: {start_npc_code: {eq: $code}}) {
      items {
        ...QuestsList_Fragment
      }
    }
  }
`)

const makeQueryOptions = (code: string) =>
  queryOptions({
    queryKey: ["npc", code],
    queryFn: async () => gqlClient.request(npcDetailedDocument, {code}),
  })

export const Route = createFileRoute("/database/(actors)/npc/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.npc) throw notFound()
    }),
  component: RouteComponent,
})

function RouteComponent() {
  const {code} = Route.useParams()
  const {
    data: {npc, maps, quests},
  } = useSuspenseQuery(makeQueryOptions(code))
  if (!npc) throw notFound()

  const details = useMemo(
    () => [
      {
        label: "Level",
        value: npc.level.toString(),
      },
      {
        label: "HP",
        value: npc.health_points.toLocaleString(),
      },
      {
        label: "Area",
        value: npc.is_sea ? "Sea" : "Land",
      },
    ],
    [npc],
  )

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...npcBreadcrumbItems,
            {label: npc.name, href: Route.fullPath},
          ]}
        />
        <PageTitle
          left={
            <ItemIcon
              variant="no-hover"
              iconName={npc.icon}
              actorGrade={npc.grade}
            />
          }
          title={npc.name}
        />
      </PageHeader>

      <ColsWrapper>
        <div>
          {npc.models && <ModelCard models={npc.models} />}
          <DetailsCard details={details} />
          <MapCard
            maps={maps.items.map((map) => ({
              map,
              positions: npc.positions.filter(
                (pos) => pos.map_code === map.code,
              ),
            }))}
          />
        </div>
        <div>
          <NPCStoreCard storeItems={npc.store_items} />
        </div>
        <div>
          <QuestsListCard quests={quests.items} />
        </div>
      </ColsWrapper>
    </>
  )
}
