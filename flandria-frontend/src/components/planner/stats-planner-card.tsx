import {cn} from "@/lib/utils"

import {clamp} from "@/utils/utils"

import {BaseClassType} from "@/gql/graphql"

import {Combobox} from "@/components/combobox"
import {
  calculateAvoidance,
  calculateMagicCriticalRate,
  calculateMagicHitRate,
  calculateMagicMaxAttack,
  calculateMagicMinAttack,
  calculateMaxHP,
  calculateMaxMP,
  calculateMeleeCriticalRate,
  calculateMeleeHitRate,
  calculateMeleeMaxAttack,
  calculateMeleeMinAttack,
  calculateRangedCriticalRate,
  calculateRangedHitRate,
  calculateRangedMaxAttack,
  calculateRangedMinAttack,
} from "@/components/planner/stat-helpers"
import {Button} from "@/components/ui/button"
import {Card, CardContent, CardFooter, CardHeader} from "@/components/ui/card"
import {Label} from "@/components/ui/label"

import {
  landLevelOptions,
  seaLevelOptions,
} from "@/routes/planner/-combobox-options"
import {MinusIcon, PlusIcon} from "lucide-react"
import * as React from "react"

const MAX_INVEST_POINTS = 500

const BASE_POINTS = {
  [BaseClassType.Explorer]: {
    strength: 19,
    dexterity: 18,
    constitution: 16,
    intelligence: 13,
    wisdom: 10,
    will: 17,
  },
  [BaseClassType.Noble]: {
    strength: 11,
    dexterity: 16,
    constitution: 12,
    intelligence: 21,
    wisdom: 19,
    will: 14,
  },
  [BaseClassType.Saint]: {
    strength: 14,
    dexterity: 14,
    constitution: 14,
    intelligence: 16,
    wisdom: 19,
    will: 16,
  },
  [BaseClassType.Mercenary]: {
    strength: 21,
    dexterity: 15,
    constitution: 22,
    intelligence: 8,
    wisdom: 10,
    will: 17,
  },
}

type StatsPlannerState = {
  levelLand: number
  levelSea: number
  strength: number
  dexterity: number
  constitution: number
  intelligence: number
  wisdom: number
  will: number
}

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
          const newValue = clamp(value + increment, 0, MAX_INVEST_POINTS)
          setValue(newValue)
        }}
      >
        <MinusIcon className="icon-size" />
      </Button>
      <span>{displayValue}</span>
      <Button
        onClick={(event) => {
          const increment = event.shiftKey ? 15 : 1
          const newValue = clamp(value + increment, 0, MAX_INVEST_POINTS)
          setValue(newValue)
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

type StatsPlannerCardProps = {
  baseClass: Exclude<BaseClassType, BaseClassType.Ship>
}
export function StatsPlannerCard({baseClass}: StatsPlannerCardProps) {
  const [
    {
      levelLand,
      levelSea,
      strength,
      dexterity,
      constitution,
      intelligence,
      wisdom,
      will,
    },
    setState,
  ] = React.useReducer<
    React.Reducer<
      StatsPlannerState,
      | Partial<StatsPlannerState>
      | ((prev: StatsPlannerState) => Partial<StatsPlannerState>)
    >
  >(
    (state, newState) => {
      const newWithPrevState =
        typeof newState === "function" ? newState(state) : newState
      const completeNewState = {...state, ...newWithPrevState}
      return completeNewState
    },
    {
      levelLand: 1,
      levelSea: 1,
      strength: 0,
      dexterity: 0,
      constitution: 0,
      intelligence: 0,
      wisdom: 0,
      will: 0,
    },
  )

  // Load hash, has to be before update hash
  React.useEffect(() => {
    const currentSearchParams = new URLSearchParams(window.location.search)
    const hash = currentSearchParams.get("s") ?? null
    if (hash === null) return
    const asJson = atob(hash)
    const data = JSON.parse(asJson) as StatsPlannerState
    setState(data)
  }, [])

  // Update hash on change
  React.useEffect(() => {
    const isInitialState =
      levelLand === 1 &&
      levelSea === 1 &&
      strength === 0 &&
      dexterity === 0 &&
      constitution === 0 &&
      intelligence === 0 &&
      wisdom === 0 &&
      will === 0

    const currentSearchParams = new URLSearchParams(window.location.search)
    if (isInitialState) {
      currentSearchParams.delete("s")
    } else {
      const asJson = JSON.stringify({
        levelLand,
        levelSea,
        strength,
        dexterity,
        constitution,
        intelligence,
        wisdom,
        will,
      })
      const hash = btoa(asJson)
      currentSearchParams.set("s", hash)
    }
    const newUrl = [window.location.pathname, currentSearchParams.toString()]
      .filter(Boolean)
      .join("?")
    window.history.replaceState(null, "", newUrl)
  }, [
    levelLand,
    levelSea,
    strength,
    dexterity,
    constitution,
    intelligence,
    wisdom,
    will,
  ])

  const calculateAvailableStatusPoints = () => {
    const seaPoints = levelSea - 1
    const landPoints = levelLand * 3
    return seaPoints + landPoints
  }

  const availablePoints = calculateAvailableStatusPoints()
  const usedPoints =
    strength + intelligence + dexterity + wisdom + constitution + will
  const remainingPoints = availablePoints - usedPoints

  const classInitialStatusPoints = BASE_POINTS[baseClass]
  const totalStrength = classInitialStatusPoints["strength"] + strength
  const totalIntelligence =
    classInitialStatusPoints["intelligence"] + intelligence
  const totalDexterity = classInitialStatusPoints["dexterity"] + dexterity
  const totalWisdom = classInitialStatusPoints["wisdom"] + wisdom
  const totalConstitution =
    classInitialStatusPoints["constitution"] + constitution
  const totalWill = classInitialStatusPoints["will"] + will

  const maxHP = Math.floor(
    calculateMaxHP(levelLand, baseClass, totalConstitution),
  )
  const maxMP = Math.floor(calculateMaxMP(levelLand, baseClass, totalWisdom))
  const avoidance = Math.floor(
    calculateAvoidance(levelLand, baseClass, totalDexterity),
  )
  const meleeMinAttack = Math.floor(
    calculateMeleeMinAttack(
      levelLand,
      baseClass,
      totalStrength,
      totalIntelligence,
    ),
  )
  const meleeMaxAttack = Math.floor(
    calculateMeleeMaxAttack(
      levelLand,
      baseClass,
      totalStrength,
      totalIntelligence,
    ),
  )
  const meleeHitrate = Math.floor(
    calculateMeleeHitRate(levelLand, baseClass, totalDexterity),
  )
  const meleeCriticalRate = Math.floor(
    calculateMeleeCriticalRate(levelLand, baseClass, totalWill),
  )
  const rangeMinAttack = Math.floor(
    calculateRangedMinAttack(
      levelLand,
      baseClass,
      totalStrength,
      totalIntelligence,
    ),
  )
  const rangeMaxAttack = Math.floor(
    calculateRangedMaxAttack(
      levelLand,
      baseClass,
      totalStrength,
      totalIntelligence,
    ),
  )
  const rangeHitrate = Math.floor(
    calculateRangedHitRate(levelLand, baseClass, totalDexterity),
  )
  const rangeCriticalRate = Math.floor(
    calculateRangedCriticalRate(levelLand, baseClass, totalWill),
  )
  const magicMinAttack = Math.floor(
    calculateMagicMinAttack(levelLand, baseClass, totalIntelligence),
  )
  const magicMaxAttack = Math.floor(
    calculateMagicMaxAttack(levelLand, baseClass, totalIntelligence),
  )
  const magicHitrate = Math.floor(
    calculateMagicHitRate(
      levelLand,
      baseClass,
      totalDexterity,
      totalIntelligence,
    ),
  )
  const magicCriticalRate = Math.floor(
    calculateMagicCriticalRate(levelLand, baseClass, totalWill),
  )

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
                setState({levelLand: parseInt(value, 10)})
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
                setState({levelSea: parseInt(value, 10)})
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
          <StatSection
            label="Strength"
            value={strength}
            displayValue={totalStrength.toString()}
            setValue={(val) => setState({strength: val})}
          />
          <StatSection
            label="Intelligence"
            value={intelligence}
            displayValue={totalIntelligence.toString()}
            setValue={(val) => setState({intelligence: val})}
          />
          <StatSection
            label="Dexterity"
            value={dexterity}
            displayValue={totalDexterity.toString()}
            setValue={(val) => setState({dexterity: val})}
          />
          <StatSection
            label="Wisdom"
            value={wisdom}
            displayValue={totalWisdom.toString()}
            setValue={(val) => setState({wisdom: val})}
          />
          <StatSection
            label="Constitution"
            value={constitution}
            displayValue={totalConstitution.toString()}
            setValue={(val) => setState({constitution: val})}
          />
          <StatSection
            label="Will"
            value={will}
            displayValue={totalWill.toString()}
            setValue={(val) => setState({will: val})}
          />
        </div>
        <div className="border-t">
          <div className="grid grid-cols-1 gap-x-8 gap-y-4 px-6 py-4 xl:grid-cols-2">
            <div>
              <StatDisplaySection
                label="Max. HP"
                value={maxHP.toLocaleString()}
                labelClassName="text-red-500"
              />
              <StatDisplaySection
                label="Max. MP"
                value={maxMP.toLocaleString()}
                labelClassName="text-blue-500"
              />
              <StatDisplaySection
                label="Avoidance"
                value={avoidance.toLocaleString()}
              />
            </div>
            <div>
              <StatDisplaySection
                label="Melee Attack"
                value={`${meleeMinAttack.toLocaleString()} ~ ${meleeMaxAttack.toLocaleString()}`}
              />
              <StatDisplaySection
                label="Melee Hitrate"
                value={meleeHitrate.toLocaleString()}
              />
              <StatDisplaySection
                label="Melee Critical Rate"
                value={meleeCriticalRate.toLocaleString()}
              />
            </div>
            <div>
              <StatDisplaySection
                label="Range Attack"
                value={`${rangeMinAttack.toLocaleString()} ~ ${rangeMaxAttack.toLocaleString()}`}
              />
              <StatDisplaySection
                label="Range Hitrate"
                value={rangeHitrate.toLocaleString()}
              />
              <StatDisplaySection
                label="Range Critical Rate"
                value={rangeCriticalRate.toLocaleString()}
              />
            </div>
            <div>
              <StatDisplaySection
                label="Magic Attack"
                value={`${magicMinAttack.toLocaleString()} ~ ${magicMaxAttack.toLocaleString()}`}
              />
              <StatDisplaySection
                label="Magic Hitrate"
                value={magicHitrate.toLocaleString()}
              />
              <StatDisplaySection
                label="Magic Critical Rate"
                value={magicCriticalRate.toLocaleString()}
              />
            </div>
          </div>
        </div>
      </CardContent>
      <CardFooter className="flex items-center justify-around border-t p-1">
        <p className="text-xs text-muted-foreground">
          Click ± 1. Shift-Click ± 15.
        </p>
        <span className="text-xs text-muted-foreground">
          Results may vary by ±1. <strong>Not</strong> affected by skill tree.
        </span>
      </CardFooter>
    </Card>
  )
}
