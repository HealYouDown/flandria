import {formatSeconds} from "@/utils/date-helpers"
import {monsterGradeToString} from "@/utils/format-helpers"

import {graphql} from "@/gql"
import {
  MapCanvas_MapDetailsFragmentFragment,
  MapCanvas_MonsterPositionFragmentFragment,
  MapCanvas_NpcPositionFragmentFragment,
} from "@/gql/graphql"

import {GridItem} from "./grid-item"

import * as React from "react"
import {Circle, Image, Layer, Stage} from "react-konva"
import {Html} from "react-konva-utils"
import useImage from "use-image"
import {useResizeObserver} from "usehooks-ts"

graphql(`
  fragment MapCanvas_MonsterPositionFragment on MonsterPosition {
    __typename
    index
    amount
    respawn_time
    x
    y
    # z
    monster {
      code
      name
      icon
      grade
      level
      # is_sea
    }
  }
`)
export type MonsterPosition = MapCanvas_MonsterPositionFragmentFragment

graphql(`
  fragment MapCanvas_NPCPositionFragment on NpcPosition {
    __typename
    index
    x
    y
    # z
    npc {
      code
      name
      icon
      grade
      level
      is_sea
    }
  }
`)
export type NPCPosition = MapCanvas_NpcPositionFragmentFragment

graphql(`
  fragment MapCanvas_MapDetailsFragment on Map {
    code
    name

    top
    left
    width
    height
  }
`)
export type MapCanvasDetails = MapCanvas_MapDetailsFragmentFragment

type MapCanvasTooltipData = {
  x: number
  y: number
  edge: MonsterPosition | NPCPosition
}

const Tooltip = ({edge}: MapCanvasTooltipData) => {
  const isMonster = edge.__typename === "MonsterPosition"
  let actor
  if (isMonster) actor = edge.monster
  else actor = edge.npc

  return (
    <GridItem.NonLinkItem className="z-10 max-w-[250px] rounded-md bg-accent px-2 py-1">
      <GridItem.Icon
        size="medium"
        variant="no-hover"
        iconName={actor.icon}
        actorGrade={actor.grade}
      />
      <GridItem.Details>
        <GridItem.Name>
          {isMonster && edge.amount > 1 ? `${edge.amount}x ` : null}
          {actor.name}
        </GridItem.Name>
        <GridItem.Subs
          subs={[
            `Lv. ${actor.level}`,
            // actor.is_sea ? "Sea" : "Land",
            isMonster ? monsterGradeToString(actor.grade) : null,
            isMonster ? `Spawn: ${formatSeconds(edge.respawn_time)}` : null,
          ]}
        />
      </GridItem.Details>
    </GridItem.NonLinkItem>
  )
}

type MapCanvasProps = {
  map: MapCanvasDetails
  positions: (MonsterPosition | NPCPosition)[]
  getColor: (code: string) => string
  dotSizeDivisor?: number
}

export function MapCanvas({
  map,
  positions,
  getColor,
  dotSizeDivisor = 70,
}: MapCanvasProps) {
  const [positionTooltipData, setPositionTooltipData] =
    React.useState<MapCanvasTooltipData | null>(null)

  const ref = React.useRef<HTMLDivElement>(null)
  const {width = 0} = useResizeObserver({ref})
  const [mapImage] = useImage(`/maps/${map.code}.png`)

  const {top: mapTop, left: mapLeft, width: mapWidth, height: mapHeight} = map
  const dotSize = width / dotSizeDivisor

  return (
    <div ref={ref} className="h-full w-full">
      <Stage width={width} height={width}>
        <Layer>
          <Image
            image={mapImage}
            width={width}
            height={width}
            alt={`${map.name} map image`}
          />
        </Layer>
        <Layer>
          {positions.map((positionElement) => {
            const {x, y} = positionElement
            const relativeX = ((x - mapLeft) / mapWidth) * width
            const relativeY = ((mapTop - y) / mapHeight) * width
            const xCentered = relativeX + dotSize / 2
            const yCentered = relativeY + dotSize / 2

            const code =
              positionElement.__typename === "MonsterPosition"
                ? positionElement.monster.code
                : positionElement.npc.code

            return (
              <Circle
                key={`${code}-${positionElement.index}`}
                // Center dot on position
                x={xCentered}
                y={yCentered}
                width={dotSize}
                height={dotSize}
                fill={getColor(code)}
                onMouseOver={() => {
                  setPositionTooltipData({
                    x: xCentered,
                    y: yCentered + dotSize / 2,
                    edge: positionElement,
                  })
                }}
                onMouseOut={() => setPositionTooltipData(null)}
              />
            )
          })}
        </Layer>
        <Layer>
          {positionTooltipData && (
            <Html
              transformFunc={(attrs) => ({
                ...attrs,
                x: positionTooltipData.x,
                y: positionTooltipData.y,
              })}
            >
              <Tooltip {...positionTooltipData} />
            </Html>
          )}
        </Layer>
      </Stage>
    </div>
  )
}
