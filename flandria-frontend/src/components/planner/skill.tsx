import {clamp} from "@/utils/utils"

import Konva from "konva"
import {Filter} from "konva/lib/Node"
import React from "react"
import {isMobile} from "react-device-detect"
import {Group, Image, Rect, Text} from "react-konva"
import useImage from "use-image"

interface SkillProps<TCode> {
  code: TCode
  icon: string
  x: number
  y: number
  canBeSkilled: boolean
  currentLevel: number
  currentMaxLevel: number
  skillMaxLevel: number
  setSkillLevel: (code: TCode, level: number) => void
  onMouseOver: () => void
  onMouseOut: () => void
}

export function Skill<T>({
  code,
  icon,
  x,
  y,
  canBeSkilled,
  currentLevel,
  currentMaxLevel,
  skillMaxLevel,
  setSkillLevel,
  onMouseOver,
  onMouseOut,
}: SkillProps<T>) {
  const [skillImage] = useImage(`/assets/icons/${icon}`)
  const [minusBtnImage] = useImage("/planner-minus-button.png")
  const [plusBtnImage] = useImage("/planner-plus-button.png")

  const imageRef = React.useRef<Konva.Image>(null)

  React.useEffect(() => {
    if (skillImage && imageRef.current) {
      imageRef.current.cache()
    }
  }, [skillImage])

  const filters: Filter[] = []
  if (currentLevel === 0) {
    if (canBeSkilled) {
      filters.push(Konva.Filters.Brighten)
    } else {
      filters.push(Konva.Filters.Grayscale)
    }
  }

  const onLevelUp = (isShift: boolean = false) => {
    if (canBeSkilled) {
      const newLevel = isShift ? currentMaxLevel : currentLevel + 1
      setSkillLevel(code, clamp(newLevel, 0, skillMaxLevel))
    }
  }

  const onLevelDown = (isShift: boolean = false) => {
    const newLevel = isShift ? 0 : currentLevel - 1
    setSkillLevel(code, clamp(newLevel, 0, skillMaxLevel))
  }

  return (
    <>
      {isMobile && (
        <Image
          image={minusBtnImage}
          x={x - 12}
          y={y - 1}
          height={34}
          width={12}
          onTap={() => onLevelDown()}
        />
      )}
      <Group
        x={x}
        y={y}
        onMouseOver={onMouseOver}
        onMouseOut={onMouseOut}
        onDblTap={() => onLevelDown}
        onClick={(event) => {
          const {evt} = event
          if (evt.button !== 0 && evt.button !== 2) return
          const isLeftClick = evt.button === 0

          if (isLeftClick) {
            onLevelUp(evt.shiftKey)
          } else {
            onLevelDown(evt.shiftKey)
          }
        }}
        onContextMenu={(event) => {
          event.evt.preventDefault()
        }}
        onMouseEnter={(event) => {
          const stage = event.currentTarget.getStage()
          if (stage) {
            stage.container().style.cursor = "pointer"
          }
        }}
        onMouseLeave={(event) => {
          const stage = event.currentTarget.getStage()
          if (stage) {
            stage.container().style.cursor = "default"
          }
        }}
      >
        <Image
          ref={imageRef}
          image={skillImage}
          filters={filters}
          width={32}
          height={32}
          brightness={-0.3}
        />

        <Group y={32 - 12} opacity={0.8}>
          <Rect fill="black" width={13} height={12} />
          <Text
            y={1}
            width={13}
            fontSize={10}
            height={12}
            fill="white"
            align="center"
            verticalAlign="center"
            text={currentLevel.toString()}
          />
        </Group>
      </Group>
      {isMobile && (
        <Image
          image={plusBtnImage}
          x={x + 32}
          y={y - 1}
          height={34}
          width={12}
          onTap={() => onLevelUp()}
        />
      )}
    </>
  )
}
