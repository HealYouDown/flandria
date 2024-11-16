import {formatSeconds} from "@/utils/date-helpers"
import {
  characterClassStringFromObject,
  formatSkillRequiredWeapons,
  rangeToMeters,
  shipClassFromObject,
} from "@/utils/format-helpers"

import {LevelSkillData} from "@/components/planner/skill-planner-card"
import {Separator} from "@/components/ui/separator"

import React from "react"

const DataPair = ({label, value}: {label: string; value: string}) => {
  return (
    <div className="flex items-center justify-between">
      <dt className="font-semibold">{label}</dt>
      <dd>{value}</dd>
    </div>
  )
}

function SkillDataSection({skillData}: {skillData: LevelSkillData[number]}) {
  const isSeaSkill = skillData.required_level_sea > 0
  const meterFactor = isSeaSkill ? 10 : 100

  return (
    <>
      <dl className="grid grid-cols-2 gap-x-8 gap-y-1 text-sm">
        <DataPair
          label="Req. Level"
          value={
            isSeaSkill
              ? skillData.required_level_sea.toString()
              : skillData.required_level_land.toString()
          }
        />
        <DataPair
          label="Cooldown"
          value={
            skillData.cooldown > 0
              ? formatSeconds(skillData.cooldown, true)
              : "/"
          }
        />
        <DataPair label="MP" value={skillData.mana_cost.toLocaleString()} />
        <DataPair
          label="Cast Time"
          value={
            skillData.cast_time > 0
              ? formatSeconds(skillData.cast_time, true)
              : "Instant"
          }
        />
        <DataPair
          label="Cast Range"
          value={
            skillData.cast_distance > 0
              ? `${rangeToMeters(skillData.cast_distance, meterFactor)}m`
              : "/"
          }
        />
        <DataPair
          label="Effect Range"
          value={
            skillData.effect_range > 0
              ? `${rangeToMeters(skillData.effect_range, meterFactor)}m`
              : "/"
          }
        />
      </dl>

      <p className="my-1 text-sm text-muted-foreground">
        {skillData.description.split("\\n").map((text, i) => (
          <React.Fragment key={i}>
            {i >= 1 && <br />}
            {text}
          </React.Fragment>
        ))}
      </p>
    </>
  )
}

type SkillTooltipProps = {
  skillCode: string
  currentLevel: number
  skillData: LevelSkillData
}

export function SkillPlannerTooltip({
  currentLevel,
  skillData,
}: SkillTooltipProps) {
  const baseSkillData = skillData[0]
  const maxLevel = baseSkillData.skill_max_level
  const isMaxLevel = currentLevel === maxLevel

  const currentSkillData = skillData[currentLevel]
  const nextSkillData = isMaxLevel ? null : skillData[currentLevel + 1]

  return (
    <div className="w-[360px] rounded-md border-2 bg-background/70 px-4 py-2 backdrop-blur-sm">
      <div className="flex items-center justify-between">
        <span className="font-bold tracking-tight text-green-400">
          {baseSkillData.name}
        </span>
        <span className="text-orange-400">
          {currentLevel}/{maxLevel}
        </span>
      </div>

      <div className="flex flex-col text-sm leading-none">
        <span>
          {" "}
          {characterClassStringFromObject(baseSkillData)}
          {shipClassFromObject(baseSkillData)}
        </span>
        <span>
          {formatSkillRequiredWeapons(baseSkillData.required_weapons)}
        </span>
      </div>

      {currentLevel > 0 && (
        <>
          <Separator className="my-2" />
          <SkillDataSection skillData={currentSkillData} />
        </>
      )}

      {nextSkillData !== null && (
        <>
          <Separator className="my-2" />
          <p className="my-2 text-center text-xs text-muted-foreground">
            Next Level: {currentLevel + 1}
          </p>
          <SkillDataSection skillData={nextSkillData} />
        </>
      )}
    </div>
  )
}
