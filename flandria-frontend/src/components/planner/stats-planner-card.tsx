import {BaseClassType} from "@/lib/enums"
import {cn} from "@/lib/utils"

import {clamp} from "@/utils/utils"

import {Combobox} from "@/components/combobox"
import * as formulas from "@/components/planner/stat-formulas.generated"
import {
  BASE_STATS,
  InvestedStats,
  MAX_INVEST_POINTS,
  SEA_LEVEL_STAT_POINT_CAP,
  availableStatPoints,
  toCharacterStats,
} from "@/components/planner/stat-helpers"
import {Button} from "@/components/ui/button"
import {Card, CardContent, CardFooter, CardHeader} from "@/components/ui/card"
import {Label} from "@/components/ui/label"

import {
  landLevelOptions,
  seaLevelOptions,
} from "@/routes/planner/-combobox-options"
import {MinusIcon, PlusIcon} from "lucide-react"

type StatSectionProps = {
  label: string
  value: number
  displayValue: string
  setValue: (n: number) => void
}

const StatSection = ({
  label,
  value,
  displayValue,
  setValue,
}: StatSectionProps) => {
  return (
    <div className="flex items-center space-x-0.5">
      <span className="grow">{label}</span>
      <Button
        size="icon"
        variant="ghost"
        onClick={(event) => {
          const increment = event.shiftKey ? -15 : -1
          setValue(clamp(value + increment, 0, MAX_INVEST_POINTS))
        }}
      >
        <MinusIcon className="icon-size" />
      </Button>
      <span>{displayValue}</span>
      <Button
        onClick={(event) => {
          const increment = event.shiftKey ? 15 : 1
          setValue(clamp(value + increment, 0, MAX_INVEST_POINTS))
        }}
        size="icon"
        variant="ghost"
      >
        <PlusIcon className="icon-size" />
      </Button>
    </div>
  )
}

type StatDisplaySectionProps = {
  label: string
  value: string
  labelClassName?: string
}

const StatDisplaySection = ({
  label,
  value,
  labelClassName,
}: StatDisplaySectionProps) => {
  return (
    <div className="grid grid-cols-2 gap-x-0.5">
      <span className={cn("font-semibold tracking-tight", labelClassName)}>
        {label}
      </span>
      <span className="text-right">{value}</span>
    </div>
  )
}

const STAT_LABELS: [keyof InvestedStats, string][] = [
  ["strength", "Strength"],
  ["intelligence", "Intelligence"],
  ["dexterity", "Dexterity"],
  ["wisdom", "Wisdom"],
  ["constitution", "Constitution"],
  ["will", "Will"],
]

type StatsPlannerCardProps = {
  baseClass: Exclude<BaseClassType, BaseClassType.Ship>
  // The selected second class, or the base class
  statClass: formulas.StatClass
  levelLand: number
  levelSea: number
  stats: InvestedStats
  onChange: (
    change: Partial<{
      levelLand: number
      levelSea: number
      stats: InvestedStats
    }>,
  ) => void
}

export function StatsPlannerCard({
  baseClass,
  statClass,
  levelLand,
  levelSea,
  stats,
  onChange,
}: StatsPlannerCardProps) {
  const usedPoints = Object.values(stats).reduce((a, b) => a + b, 0)
  const remainingPoints = availableStatPoints(levelLand, levelSea) - usedPoints

  const baseStats = BASE_STATS[baseClass]
  const totals = Object.fromEntries(
    STAT_LABELS.map(([key]) => [key, baseStats[key] + stats[key]]),
  ) as InvestedStats

  const s = toCharacterStats(totals)
  const calc = (fn: typeof formulas.maxHP) =>
    fn(statClass, levelLand, s).toLocaleString()
  const range = (min: typeof formulas.maxHP, max: typeof formulas.maxHP) =>
    `${calc(min)} ~ ${calc(max)}`

  return (
    <Card className="w-full max-w-[450px] xl:w-auto xl:max-w-max">
      <CardHeader>
        <div className="flex flex-row items-center space-x-2">
          <div className="flex grow flex-col space-y-0.5">
            <Label htmlFor="levelLand">Level Land</Label>
            <Combobox
              id="landLevel"
              triggerClassName="w-full"
              contentClassName="popover-content-width-full"
              nullable={false}
              options={landLevelOptions}
              value={levelLand.toString()}
              onValueChange={(value) =>
                onChange({levelLand: parseInt(value, 10)})
              }
            />
          </div>
          <div className="flex grow flex-col space-y-0.5">
            <Label htmlFor="seaLevel">Level Sea</Label>
            <Combobox
              id="seaLevel"
              triggerClassName="w-full"
              contentClassName="popover-content-width-full"
              nullable={false}
              options={seaLevelOptions}
              value={levelSea.toString()}
              onValueChange={(value) =>
                onChange({levelSea: parseInt(value, 10)})
              }
            />
          </div>
        </div>
        <div
          className={cn(
            "flex items-center justify-around",
            remainingPoints < 0 ? "text-red-500" : undefined,
          )}
        >
          <p>Remaining: {remainingPoints}</p>
          <p>Used: {usedPoints}</p>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <div className="grid grid-cols-1 gap-x-4 px-6 py-4 xl:grid-cols-2">
          {STAT_LABELS.map(([key, label]) => (
            <StatSection
              key={key}
              label={label}
              value={stats[key]}
              displayValue={totals[key].toString()}
              setValue={(val) => onChange({stats: {...stats, [key]: val}})}
            />
          ))}
        </div>
        <div className="border-t">
          <div className="grid grid-cols-1 gap-x-8 gap-y-4 px-6 py-4 xl:grid-cols-2">
            <div>
              <StatDisplaySection
                label="Max. HP"
                value={calc(formulas.maxHP)}
                labelClassName="text-red-500"
              />
              <StatDisplaySection
                label="Max. MP"
                value={calc(formulas.maxMP)}
                labelClassName="text-blue-500"
              />
              <StatDisplaySection
                label="Avoidance"
                value={calc(formulas.avoidance)}
              />
            </div>
            <div>
              <StatDisplaySection
                label="Melee Attack"
                value={range(formulas.meleeMinAttack, formulas.meleeMaxAttack)}
              />
              <StatDisplaySection
                label="Melee Hitrate"
                value={calc(formulas.meleeHitRate)}
              />
              <StatDisplaySection
                label="Melee Critical Rate"
                value={calc(formulas.meleeCriticalRate)}
              />
            </div>
            <div>
              <StatDisplaySection
                label="Range Attack"
                value={range(formulas.rangeMinAttack, formulas.rangeMaxAttack)}
              />
              <StatDisplaySection
                label="Range Hitrate"
                value={calc(formulas.rangeHitRate)}
              />
              <StatDisplaySection
                label="Range Critical Rate"
                value={calc(formulas.rangeCriticalRate)}
              />
            </div>
            <div>
              <StatDisplaySection
                label="Magic Attack"
                value={range(formulas.magicMinAttack, formulas.magicMaxAttack)}
              />
              <StatDisplaySection
                label="Magic Hitrate"
                value={calc(formulas.magicHitRate)}
              />
              <StatDisplaySection
                label="Magic Critical Rate"
                value={calc(formulas.magicCriticalRate)}
              />
            </div>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex flex-col items-center border-t p-1 text-center text-xs text-muted-foreground">
        <p>
          Click ± 1. Shift-Click ± 15. <strong>Not</strong> affected by skill
          tree.
        </p>
        {levelSea > SEA_LEVEL_STAT_POINT_CAP && (
          <p>
            Sea levels above {SEA_LEVEL_STAT_POINT_CAP} don't grant stat points.
          </p>
        )}
      </CardFooter>
    </Card>
  )
}
