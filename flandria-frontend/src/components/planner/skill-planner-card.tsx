import {useTheme} from "@/lib/theme-provider"
import {cn} from "@/lib/utils"

import {Combobox, ComboboxOption} from "@/components/combobox"
import {Skill} from "@/components/planner/skill"
import {
  CLASS_MIN_LEVEL,
  ClassFlagsType,
  SKILL_PLANNER_HEIGHT,
  SKILL_PLANNER_WIDTH,
  SkillBuild,
  SkillTree,
  canLevelUpSkill,
  getAvailableSkillPoints,
  maxReachableSkillLevel,
  normalizeSkillBuild,
  setSkillLevel,
  usedSkillPoints,
} from "@/components/planner/skill-helpers"
import {SkillPlannerTooltip} from "@/components/planner/skill-tooltip"
import {Button} from "@/components/ui/button"
import {Card, CardContent, CardFooter, CardHeader} from "@/components/ui/card"

import {useToast} from "@/hooks/use-toast"
import Konva from "konva"
import {DownloadIcon, LinkIcon} from "lucide-react"
import * as React from "react"
import {isMobile} from "react-device-detect"
import {Image, Layer, Rect, Stage} from "react-konva"
import {Html} from "react-konva-utils"
import useImage from "use-image"

type SkillPositions<TCode extends string> = {
  [key in TCode]: {
    x: number
    y: number
  }
}

type SkillPlannerCardProps<TCode extends string> = {
  tree: SkillTree<TCode>
  build: SkillBuild<TCode>
  onChange: (build: SkillBuild<TCode>) => void
  positions: SkillPositions<TCode>
  background: "ship" | "explorer" | "noble" | "saint" | "mercenary"
  classOptions: ComboboxOption<ClassFlagsType>[] | null
  levelOptions: ComboboxOption<string>[]
}

export function SkillPlannerCard<TCode extends string>({
  tree,
  build,
  onChange,
  positions,
  background,
  classOptions,
  levelOptions,
}: SkillPlannerCardProps<TCode>) {
  const {toast} = useToast()
  const {theme} = useTheme()
  const stageRef = React.useRef<Konva.Stage>(null)
  const [hoveredSkillCode, setHoveredSkillCode] = React.useState<TCode | null>(
    null,
  )
  const [bgImage] = useImage(`/planner-trees/${background}-lines.png`)

  const skillCodes = Object.keys(tree.skills) as TCode[]
  const {level, class: selectedClass, skills: skillLevels} = build

  const exportTreeAsImage = (): void => {
    if (!stageRef.current) return

    const uri = stageRef.current.toDataURL({pixelRatio: 2.0})

    // Hacky way to download from data dataURI
    const link = document.createElement("a")
    link.href = uri
    link.download = `skilltree-${background}.png`
    link.click()
  }

  const usedPoints = usedSkillPoints(skillLevels)
  const remainingSkillPoints = getAvailableSkillPoints(level) - usedPoints

  return (
    <Card className="max-w-min">
      <CardHeader>
        <div className="flex flex-row items-center space-x-2">
          <Combobox
            id="level"
            triggerClassName="w-full"
            contentClassName="popover-content-width-full"
            nullable={false}
            options={levelOptions}
            value={level.toString()}
            onValueChange={(value) =>
              onChange(
                normalizeSkillBuild(
                  {...build, level: parseInt(value, 10)},
                  tree,
                ),
              )
            }
          />
          {classOptions !== null && (
            <Combobox
              nullable
              disabled={level < CLASS_MIN_LEVEL}
              placeholder="Select class..."
              id="class"
              triggerClassName="w-full"
              contentClassName="popover-content-width-full"
              options={classOptions}
              value={selectedClass}
              onValueChange={(s) =>
                onChange(normalizeSkillBuild({...build, class: s}, tree))
              }
            />
          )}
        </div>
        <div
          className={cn(
            "flex items-center justify-around",
            remainingSkillPoints < 0 ? "text-red-500" : undefined,
          )}
        >
          <p>Remaining: {remainingSkillPoints}</p>
          <p>Used: {usedPoints}</p>
        </div>
      </CardHeader>
      <CardContent className={cn("p-0", isMobile ? "overflow-x-auto" : null)}>
        <div>
          <Stage
            ref={stageRef}
            width={SKILL_PLANNER_WIDTH}
            height={SKILL_PLANNER_HEIGHT}
          >
            <Layer>
              <Rect
                width={SKILL_PLANNER_WIDTH}
                height={SKILL_PLANNER_HEIGHT}
                fill={theme === "dark" ? "#09090b" : "#ffffff"}
              />
              <Image
                image={bgImage}
                width={SKILL_PLANNER_WIDTH}
                height={SKILL_PLANNER_HEIGHT}
                preventDefault={false}
              />
            </Layer>
            <Layer>
              {skillCodes.map((skillCode: TCode) => {
                const {x, y} = positions[skillCode]
                const currentSkillLevel = skillLevels[skillCode]

                const skillData = tree.skills[skillCode]
                const {icon, skill_max_level} = skillData[0]

                return (
                  <Skill
                    key={skillCode}
                    code={skillCode}
                    x={x}
                    y={y}
                    icon={icon}
                    canBeSkilled={canLevelUpSkill(build, tree, skillCode)}
                    currentLevel={currentSkillLevel}
                    skillMaxLevel={skill_max_level}
                    currentMaxLevel={maxReachableSkillLevel(skillData, level)}
                    onMouseOver={() => setHoveredSkillCode(skillCode)}
                    onMouseOut={() => setHoveredSkillCode(null)}
                    setSkillLevel={(code, newLevel) =>
                      onChange(setSkillLevel(build, tree, code, newLevel))
                    }
                  />
                )
              })}
            </Layer>
            <Layer>
              {hoveredSkillCode && !isMobile && (
                <Html
                  transformFunc={(attrs) => ({
                    ...attrs,
                    x: positions[hoveredSkillCode].x + 48,
                    y: positions[hoveredSkillCode].y - 150,
                  })}
                >
                  <SkillPlannerTooltip
                    skillCode={hoveredSkillCode}
                    skillData={tree.skills[hoveredSkillCode]}
                    currentLevel={skillLevels[hoveredSkillCode]}
                  />
                </Html>
              )}
            </Layer>
          </Stage>
        </div>
      </CardContent>
      <CardFooter className="flex items-center justify-around border-t p-1">
        <span className="text-xs text-muted-foreground">
          Click ± 1. Shift-Click Max.
        </span>
        <div>
          <Button variant="ghost" size="sm" asChild>
            <a
              href="discord://-/channels/534732272553689109/1300076329772781669"
              target="_self"
              referrerPolicy="no-referrer"
            >
              {theme === "dark" ? (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 127.14 96.36"
                  className="icon-size"
                >
                  <path
                    fill="#fff"
                    d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,0,49,6.83,72.37,72.37,0,0,0,45.64,0,105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,56.6.54,80.21h0A105.73,105.73,0,0,0,32.71,96.36,77.7,77.7,0,0,0,39.6,85.25a68.42,68.42,0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a75.57,75.57,0,0,0,64.32,0c.87.71,1.76,1.39,2.66,2a68.68,68.68,0,0,1-10.87,5.19,77,77,0,0,0,6.89,11.1A105.25,105.25,0,0,0,126.6,80.22h0C129.24,52.84,122.09,29.11,107.7,8.07ZM42.45,65.69C36.18,65.69,31,60,31,53s5-12.74,11.43-12.74S54,46,53.89,53,48.84,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.25,60,73.25,53s5-12.74,11.44-12.74S96.23,46,96.12,53,91.08,65.69,84.69,65.69Z"
                  />
                </svg>
              ) : (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 127.14 96.36"
                  className="icon-size"
                >
                  <path d="M107.7,8.07A105.15,105.15,0,0,0,81.47,0a72.06,72.06,0,0,0-3.36,6.83A97.68,97.68,0,0,0,49,6.83,72.37,72.37,0,0,0,45.64,0,105.89,105.89,0,0,0,19.39,8.09C2.79,32.65-1.71,56.6.54,80.21h0A105.73,105.73,0,0,0,32.71,96.36,77.7,77.7,0,0,0,39.6,85.25a68.42,68.42,0,0,1-10.85-5.18c.91-.66,1.8-1.34,2.66-2a75.57,75.57,0,0,0,64.32,0c.87.71,1.76,1.39,2.66,2a68.68,68.68,0,0,1-10.87,5.19,77,77,0,0,0,6.89,11.1A105.25,105.25,0,0,0,126.6,80.22h0C129.24,52.84,122.09,29.11,107.7,8.07ZM42.45,65.69C36.18,65.69,31,60,31,53s5-12.74,11.43-12.74S54,46,53.89,53,48.84,65.69,42.45,65.69Zm42.24,0C78.41,65.69,73.25,60,73.25,53s5-12.74,11.44-12.74S96.23,46,96.12,53,91.08,65.69,84.69,65.69Z" />
                </svg>
              )}
            </a>
          </Button>
          <Button variant="ghost" size="sm" onClick={exportTreeAsImage}>
            <DownloadIcon className="icon-size" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => {
              navigator.clipboard.writeText(window.location.toString())
              toast({
                title: "Link Copied!",
                description:
                  "Your build link is ready to go. Show all of Florensia your ultimate build!",
              })
            }}
          >
            <LinkIcon className="icon-size" />
          </Button>
        </div>
      </CardFooter>
    </Card>
  )
}
