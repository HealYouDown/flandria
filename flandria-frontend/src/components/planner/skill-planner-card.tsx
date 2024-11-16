import {useTheme} from "@/lib/theme-provider"
import {cn} from "@/lib/utils"

import {Combobox, ComboboxOption} from "@/components/combobox"
import {Skill} from "@/components/planner/skill"
import {
  CLASS_FLAGS,
  ClassFlagsType,
  PlayerSkill,
  SKILL_PLANNER_HEIGHT,
  SKILL_PLANNER_WIDTH,
  makeSkillLevels,
} from "@/components/planner/skill-helpers"
import {SkillPlannerTooltip} from "@/components/planner/skill-tooltip"
import {Button} from "@/components/ui/button"
import {Card, CardContent, CardFooter, CardHeader} from "@/components/ui/card"

import usePrevious from "@/hooks/use-previous"
import {useToast} from "@/hooks/use-toast"
import Konva from "konva"
import {DownloadIcon, LinkIcon} from "lucide-react"
import * as React from "react"
import {isMobile} from "react-device-detect"
import {Image, Layer, Rect, Stage} from "react-konva"
import {Html} from "react-konva-utils"
import {useDeepCompareEffect, useDeepCompareMemo} from "use-deep-compare"
import useImage from "use-image"

export type SkillLevels<TCode extends string> = {
  [key in TCode]: number
}

type SkillPositions<TCode extends string> = {
  [key in TCode]: {
    x: number
    y: number
  }
}

export type LevelSkillData = {[key: number]: PlayerSkill}

export type GroupedSkillData<TCode extends string> = {
  [key in TCode]: LevelSkillData
}

type PlannerState<TCode extends string> = {
  level: number
  class: ClassFlagsType | null
  skills: SkillLevels<TCode>
}

type SkillPlannerCardProps<TCode extends string> = {
  skillData: GroupedSkillData<TCode>
  positions: SkillPositions<TCode>
  background: "ship" | "explorer" | "noble" | "saint" | "mercenary"
  alwaysAllowedClasses: ClassFlagsType[]
  classOptions: ComboboxOption<ClassFlagsType>[] | null

  levelOptions: ComboboxOption<string>[]
  getAvailableSkillPointsFromLevel: (level: number) => number
}

export function SkillPlannerCard<TCode extends string>({
  skillData: groupedSkills,
  positions,
  background,
  alwaysAllowedClasses,
  classOptions,
  levelOptions,
  getAvailableSkillPointsFromLevel,
}: SkillPlannerCardProps<TCode>) {
  const {toast} = useToast()

  const skillCodes = useDeepCompareMemo(
    () => Object.keys(groupedSkills) as TCode[],
    [groupedSkills],
  )

  const [{level, class: selectedClass, skills: skillLevels}, setPlannerState] =
    React.useReducer<
      React.Reducer<
        PlannerState<TCode>,
        | Partial<PlannerState<TCode>>
        | ((prev: PlannerState<TCode>) => Partial<PlannerState<TCode>>)
      >
    >(
      (state, newState) => {
        const newWithPrevState =
          typeof newState === "function" ? newState(state) : newState
        const completeNewState = {...state, ...newWithPrevState}
        return completeNewState
      },
      {
        level: 1,
        class: null,
        skills: makeSkillLevels(skillCodes, 0),
      },
    )
  const [hoveredSkillCode, setHoveredSkillCode] = React.useState<TCode | null>(
    null,
  )

  const {theme} = useTheme()
  const stageRef = React.useRef<Konva.Stage>(null)
  const previousLevel = usePrevious(level)

  const [bgImage] = useImage(`/planner-trees/${background}-lines.png`)

  const allowedClassFlags: ClassFlagsType[] = [
    ...alwaysAllowedClasses,
    ...(selectedClass === null ? [] : [selectedClass]),
  ]

  const getChildSkillCodes = (parentCode: TCode): TCode[] => {
    const codes: TCode[] = []

    Object.keys(groupedSkills).forEach((code) => {
      const baseSkill = groupedSkills[code as TCode][0]
      const previousSkills = baseSkill.required_skills.map(
        (o) => o.required_skill_code as TCode,
      )
      if (previousSkills.includes(parentCode)) {
        codes.push(code as TCode)
        codes.push(...getChildSkillCodes(code as TCode))
      }
    })

    return [...new Set(codes)].filter((code) => code != parentCode)
  }

  const canSkillBeLeveled = (skillCode: TCode): boolean => {
    const baseSkillData = groupedSkills[skillCode][0]
    const currentSkillLevel = skillLevels[skillCode]

    // Check that all previous skills are at least level 1
    const previousSkillsSkilled = baseSkillData.required_skills.every(
      (s) => skillLevels[s.required_skill_code as TCode] >= 1,
    )

    // Check that the level criteria for the next level is matched
    let levelMatches = true
    if (currentSkillLevel !== baseSkillData.skill_max_level) {
      const nextSkillData = groupedSkills[skillCode][currentSkillLevel + 1]

      // We have to check whether our level is a sea or land level
      const nextSkillRequiredLevel =
        nextSkillData.required_level_land === 0
          ? nextSkillData.required_level_sea
          : nextSkillData.required_level_land
      levelMatches = level >= nextSkillRequiredLevel
    }

    // Check that any required classes is selected
    // Some skills can be skilled by multiple classes, so
    // we only check if one class is selected, not all.
    const requiredClassesSelected = CLASS_FLAGS.some((flag) => {
      // We don't require that class
      if (baseSkillData[flag] === false) {
        return null
      }
      return allowedClassFlags.includes(flag)
    })
    // Some skills (looking at you sea) also requires no class at all
    const requiresNoClass =
      CLASS_FLAGS.reduce((s, flag) => s + Number(baseSkillData[flag]), 0) === 0

    return (
      previousSkillsSkilled &&
      levelMatches &&
      (requiredClassesSelected || requiresNoClass)
    )
  }

  const setSkillLevel = (skillCode: TCode, newSkillLevel: number): void => {
    if (newSkillLevel === 0) {
      // iterate tree and get all skills after our current skill
      // => set them all to 0
      const childSkillCodes = getChildSkillCodes(skillCode)
      const skillsToReset = [skillCode as TCode, ...childSkillCodes]
      const resettedSkills = skillsToReset.reduce((acc, current) => {
        acc[current] = 0
        return acc
      }, {} as SkillLevels<TCode>)

      setPlannerState((prev) => ({skills: {...prev.skills, ...resettedSkills}}))
    } else {
      // Just set the skill level for the given skill code
      // Check that we have enough points to do so, if not,
      // just increase the skill as much as possible

      // We can always decrease skill levels
      const isLower = newSkillLevel < skillLevels[skillCode]
      if (!isLower) {
        // We don't have any points left, so return early
        if (remainingSkillPoints === 0) return

        // Cap new skill level if we don't have enough points
        const currentSkillLevel = skillLevels[skillCode]
        if (newSkillLevel > remainingSkillPoints + currentSkillLevel) {
          newSkillLevel = remainingSkillPoints + currentSkillLevel
        }
      }
      setPlannerState((prev) => ({
        skills: {...prev.skills, [skillCode]: newSkillLevel},
      }))
    }
  }

  const exportTreeAsImage = (): void => {
    if (!stageRef.current) return

    const uri = stageRef.current.toDataURL({pixelRatio: 2.0})

    // Hacky way to download from data dataURI
    const link = document.createElement("a")
    link.href = uri
    link.download = `skilltree-${background}.png`
    link.click()
  }

  // Loads the hash - if existing
  React.useEffect(() => {
    const currentSearchParams = new URLSearchParams(window.location.search)
    const hash = currentSearchParams.get("p") ?? null
    if (hash === null) return
    const asJson = atob(hash)
    const data = JSON.parse(asJson) as PlannerState<TCode>
    setPlannerState(data)
  }, [])

  // Sets the hash on update
  // Does not set the hash if everything is equal to the initial state, so that our loaded state is not overriden on the first render
  // There are probably better ways, but that's the easiest :)
  useDeepCompareEffect(() => {
    const isInitialState =
      level === 1 &&
      Object.values(skillLevels as number[]).reduce((a, b) => a + b) == 0

    const plannerState: PlannerState<TCode> = {
      level,
      skills: skillLevels,
      class: selectedClass,
    }
    const asJson = JSON.stringify(plannerState)
    const hash = btoa(asJson)
    const currentSearchParams = new URLSearchParams(window.location.search)
    if (isInitialState) {
      currentSearchParams.delete("p")
    } else {
      currentSearchParams.set("p", hash)
    }
    // Normally we would use tanstack routers navigate function, but this
    // results in a re-render / redirect every time we use it.
    // We only want to store the state in the URL, so we bypass the navigate
    // function.
    const newUrl = [window.location.pathname, currentSearchParams.toString()]
      .filter(Boolean)
      .join("?")
    window.history.replaceState(null, "", newUrl)
  }, [level, skillLevels, selectedClass])

  // Updates whenever our level changes, resets all skills. Resets class if level is now < 40.
  useDeepCompareEffect(() => {
    // Level was reduced, so we reset all skills
    if (previousLevel && level < previousLevel) {
      setPlannerState({skills: makeSkillLevels(skillCodes)})
      if (level < 40) {
        setPlannerState({class: null})
      }
    }
  }, [skillCodes, previousLevel, level])

  // Updates whenever our class changes, disables all skills that do not match the new selected class.
  useDeepCompareEffect(() => {
    if (selectedClass === null) return

    // Reset all cc skills
    const ccSkillCodes = Object.keys(groupedSkills).filter((key) => {
      const baseData = groupedSkills[key as TCode][0]
      const skillIsCC = CLASS_FLAGS.every((flag) => {
        // Skill flag is not used, so we ignore it
        if (!baseData[flag]) return true
        // Check if our skill flag is in our always on classes
        // (basically the base classes)
        // If it isn't, then it's a cc skill
        return !alwaysAllowedClasses!.includes(flag)
      })
      return skillIsCC
    })

    setPlannerState((prev) => ({
      skills: {...prev.skills, ...makeSkillLevels(ccSkillCodes)},
    }))
  }, [selectedClass, groupedSkills, alwaysAllowedClasses])

  const maxSkillPoints = getAvailableSkillPointsFromLevel(level)
  const usedSkillPoints = (Object.values(skillLevels) as number[]).reduce(
    (a, b) => a + b,
  )
  const remainingSkillPoints = maxSkillPoints - usedSkillPoints

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
              setPlannerState({level: parseInt(value, 10)})
            }
          />
          {classOptions !== null && (
            <Combobox
              nullable
              disabled={level < 40}
              placeholder="Select class..."
              id="class"
              triggerClassName="w-full"
              contentClassName="popover-content-width-full"
              options={classOptions}
              value={selectedClass}
              onValueChange={(s) => setPlannerState({class: s})}
            />
          )}
        </div>
        <div className="flex items-center justify-around">
          <p>Remaining: {remainingSkillPoints}</p>
          <p>Used: {usedSkillPoints}</p>
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

                const skillData = groupedSkills[skillCode]
                const {icon, skill_max_level} = skillData[0]
                const canBeSkilled = canSkillBeLeveled(skillCode)

                const currentMaxLevel = Math.max(
                  0,
                  ...Object.values(skillData)
                    .filter((skill) => {
                      const requiredLevel =
                        skill.required_level_land === 0
                          ? skill.required_level_sea
                          : skill.required_level_land

                      return requiredLevel <= level
                    })
                    .map((skill) => skill.skill_level),
                )

                return (
                  <Skill
                    key={skillCode}
                    code={skillCode}
                    x={x}
                    y={y}
                    icon={icon}
                    canBeSkilled={canBeSkilled}
                    currentLevel={currentSkillLevel}
                    skillMaxLevel={skill_max_level}
                    currentMaxLevel={currentMaxLevel}
                    onMouseOver={() => setHoveredSkillCode(skillCode)}
                    onMouseOut={() => setHoveredSkillCode(null)}
                    setSkillLevel={setSkillLevel}
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
                    skillData={groupedSkills[hoveredSkillCode]}
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
