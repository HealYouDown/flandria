import {gqlClient} from "@/lib/graphql-client"
import {queryClient} from "@/lib/react-query-client"

import {colorFromString} from "@/utils/color-from-string"

import {graphql} from "@/gql"
import {ActorGrade} from "@/gql/graphql"

import {GridItem} from "@/components/grid-item"
import {MapCanvas} from "@/components/map-canvas"
import {
  PageHeader,
  PageHeaderBreadcrumbs,
  PageTitle,
} from "@/components/page-header"
import {Button} from "@/components/ui/button"
import {Separator} from "@/components/ui/separator"

import {mapBreadcrumbItems} from "./map"

import {queryOptions, useSuspenseQuery} from "@tanstack/react-query"
import {createFileRoute, notFound} from "@tanstack/react-router"
import * as React from "react"

const mapDetailedQuery = graphql(`
  query MapDetailed($code: String!) {
    map(code: $code) {
      ...MapCanvas_MapDetailsFragment

      monsters {
        ...MapCanvas_MonsterPositionFragment
      }

      npcs {
        ...MapCanvas_NPCPositionFragment
      }
    }
  }
`)

const makeQueryOptions = (code: string) =>
  queryOptions({
    queryKey: ["map", code],
    queryFn: async () => gqlClient.request(mapDetailedQuery, {code}),
  })

export const Route = createFileRoute("/database/map/$code")({
  loader: ({params: {code}}) =>
    queryClient.ensureQueryData(makeQueryOptions(code)).then((resp) => {
      if (!resp.map) throw notFound()
    }),
  component: RouteComponent,
})

type ToggleButtonProps = {
  code: string
  name: string
  icon: string
  grade: ActorGrade

  isEnabled: boolean
  onClick: (code: string) => void
}
const ToggleButton = ({
  code,
  name,
  icon,
  grade,
  isEnabled,
  onClick,
}: ToggleButtonProps) => {
  return (
    <GridItem.NonLinkItem
      asChild
      className="justify-start truncate border px-2 py-1"
    >
      <Button
        variant={isEnabled ? "secondary" : "outline"}
        onClick={() => onClick(code)}
        className="h-auto"
      >
        <GridItem.Icon
          className={isEnabled ? "grayscale-0" : "grayscale"}
          variant="no-hover"
          iconName={icon}
          actorGrade={grade}
        />
        <GridItem.Details>
          <GridItem.Name className={isEnabled ? "" : "text-muted-foreground"}>
            {name}
          </GridItem.Name>
        </GridItem.Details>
      </Button>
    </GridItem.NonLinkItem>
  )
}

function RouteComponent() {
  const {code} = Route.useParams()
  const {data} = useSuspenseQuery(makeQueryOptions(code))
  const map = data.map!

  const [disabledCodes, setDisabledCodes] = React.useState<string[]>([])

  const monsterCodes = React.useMemo(
    () => [...new Set(map.monsters.map((edge) => edge.monster.code))],
    [map.monsters],
  )
  const uniqueMonsters = React.useMemo(
    () =>
      monsterCodes.map(
        (code) => map.monsters.find((edge) => edge.monster.code === code)!,
      ),
    [map.monsters, monsterCodes],
  )

  const npcCodes = React.useMemo(
    () => [...new Set(map.npcs.map((edge) => edge.npc.code))],
    [map.npcs],
  )
  const uniqueNPCs = React.useMemo(
    () =>
      npcCodes.map((code) => map.npcs.find((edge) => edge.npc.code === code)!),
    [map.npcs, npcCodes],
  )

  const isEnabled = (code: string) => !disabledCodes.includes(code)

  const setEnabled = (code: string) =>
    setDisabledCodes(disabledCodes.filter((c) => c != code))

  const setDisabled = (code: string) =>
    setDisabledCodes([...disabledCodes, code])

  const onClickHandler = (code: string) =>
    isEnabled(code) ? setDisabled(code) : setEnabled(code)

  return (
    <>
      <PageHeader>
        <PageHeaderBreadcrumbs
          items={[
            ...mapBreadcrumbItems,
            {label: map.name, href: Route.fullPath},
          ]}
        />
        <PageTitle title={map.name} />
      </PageHeader>

      <div className="flex flex-col gap-10 2xl:flex-row">
        <div className="mx-auto w-full max-w-[768px]">
          <MapCanvas
            map={map}
            positions={[...map.monsters, ...map.npcs].filter((edge) => {
              const code =
                edge.__typename === "MonsterPosition"
                  ? edge.monster.code
                  : edge.npc.code
              return isEnabled(code)
            })}
            getColor={colorFromString}
          />
        </div>

        <div className="flex grow flex-col">
          <div className="flex flex-col">
            <h2 className="mb-1 text-lg font-bold tracking-tight">NPCs</h2>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 4xl:grid-cols-3">
              {npcCodes.length === 0 && <span>No NPCs found on this map.</span>}
              {uniqueNPCs.map((edge) => {
                const npc = edge.npc
                return (
                  <ToggleButton
                    key={npc.code}
                    {...npc}
                    isEnabled={isEnabled(npc.code)}
                    onClick={onClickHandler}
                  />
                )
              })}
            </div>
          </div>

          <Separator className="my-4" />

          <div className="flex flex-col">
            <h2 className="mb-1 text-lg font-bold tracking-tight">Monsters</h2>
            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 4xl:grid-cols-3">
              {monsterCodes.length === 0 && (
                <span>No monsters found on this map.</span>
              )}
              {uniqueMonsters.map((edge) => {
                const monster = edge.monster

                return (
                  <ToggleButton
                    key={monster.code}
                    {...monster}
                    isEnabled={isEnabled(monster.code)}
                    onClick={onClickHandler}
                  />
                )
              })}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
