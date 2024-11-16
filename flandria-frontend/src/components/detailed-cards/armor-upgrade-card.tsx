import {EffectCode, UpgradeRuleFragment} from "@/gql/graphql"

import {
  Card,
  CardContentList,
  CardContentListItem,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {Slider} from "@/components/ui/slider"

import * as React from "react"

interface ArmorUpgradeCard {
  upgradeRules: UpgradeRuleFragment[]
  basePhysicalDefense: number
  baseMagicalDefense: number
  baseAttackSpeed?: number
  baseMovementSpeed?: number
  basePhysicalAvoidance?: number
  baseHitrate?: number
}

export function ArmorUpgradeCard({
  upgradeRules,
  basePhysicalDefense,
  baseMagicalDefense,
  baseAttackSpeed = -1,
  baseMovementSpeed = -1,
  basePhysicalAvoidance = -1,
  baseHitrate = -1,
}: ArmorUpgradeCard) {
  // Add empty rule for level 0 for items that do not have rules defined
  // We still want to display the stats
  const rules: UpgradeRuleFragment[] =
    upgradeRules.length > 0
      ? upgradeRules
      : [
          {
            level: 0,
            cost: 0,
            effects: [],
          },
        ]
  const maxUpgradeLevel = Math.max(...rules.map((rule) => rule.level))

  const [upgradeLevel, setUpgradeLevel] = React.useState(0)

  const currentRule =
    rules.find((rule) => rule.level == upgradeLevel) || rules[0]

  const {
    calculatedPhysicalDefense,
    calculatedMagicalDefense,
    calculatedAttackSpeed,
    calculatedHitrate,
    calculatedMovementSpeed,
    calculatedPhysicalAvoidance,
  } = React.useMemo(() => {
    let calculatedPhysicalDefense = basePhysicalDefense
    let calculatedMagicalDefense = baseMagicalDefense
    let calculatedAttackSpeed = baseAttackSpeed
    let calculatedMovementSpeed = baseMovementSpeed
    let calculatedPhysicalAvoidance = basePhysicalAvoidance
    let calculatedHitrate = baseHitrate

    currentRule.effects.forEach((effect) => {
      if (effect.effect_code === EffectCode.CharPhDefc) {
        calculatedPhysicalDefense = Math.floor(
          basePhysicalDefense + effect.value,
        )
      } else if (effect.effect_code === EffectCode.CharMagicDefc) {
        calculatedMagicalDefense = Math.floor(baseMagicalDefense + effect.value)
      } else if (effect.effect_code === EffectCode.CharAllAttackSpeed) {
        calculatedAttackSpeed = effect.value
      } else if (effect.effect_code === EffectCode.CharMoveSpd) {
        calculatedMovementSpeed = effect.value
      } else if (effect.effect_code === EffectCode.Unknown_8) {
        calculatedHitrate = Math.floor(effect.value)
      } else if (effect.effect_code === EffectCode.CharPhAvd) {
        calculatedPhysicalAvoidance = Math.floor(effect.value)
      } else {
        console.error(`Unknown effect code ${effect.effect_code}`)
      }
    })

    return {
      calculatedPhysicalDefense,
      calculatedMagicalDefense,
      calculatedAttackSpeed,
      calculatedMovementSpeed,
      calculatedHitrate,
      calculatedPhysicalAvoidance,
    }
  }, [
    currentRule,
    basePhysicalDefense,
    baseMagicalDefense,
    baseAttackSpeed,
    baseMovementSpeed,
    baseHitrate,
    basePhysicalAvoidance,
  ])

  const changedClassName = "text-green-600 dark:text-green-400"
  const isPhDefChanged = basePhysicalDefense !== calculatedPhysicalDefense
  const isMagicDefChanged = baseMagicalDefense !== calculatedMagicalDefense

  const hasAttackSpeedStat = baseAttackSpeed !== -1
  const isAttackSpeedChanged = baseAttackSpeed !== calculatedAttackSpeed

  const hasMovementSpeedStat = baseMovementSpeed !== -1
  const isMovementSpeedChanged = baseMovementSpeed !== calculatedMovementSpeed

  const hasHitrateStat = baseHitrate !== -1
  const isHitrateChanged = baseHitrate !== calculatedHitrate

  const hasPhAvoidanceStat = basePhysicalAvoidance !== -1
  const hasPhAvoidanceChanged =
    basePhysicalAvoidance !== calculatedPhysicalAvoidance

  return (
    <Card>
      <CardHeader>
        <CardTitle>Stats</CardTitle>
      </CardHeader>
      <CardContentList>
        {maxUpgradeLevel > 0 && (
          <CardContentListItem className="flex items-center space-x-2">
            <span>{upgradeLevel}</span>
            <Slider
              step={1}
              min={0}
              max={maxUpgradeLevel}
              value={[upgradeLevel]}
              onValueChange={(value) => setUpgradeLevel(value[0])}
            />
          </CardContentListItem>
        )}
        <CardContentListItem className="flex items-center justify-between space-x-4">
          <span>Physical Defense</span>
          <span className={isPhDefChanged ? changedClassName : undefined}>
            {calculatedPhysicalDefense.toLocaleString()}
          </span>
        </CardContentListItem>
        <CardContentListItem className="flex items-center justify-between space-x-4">
          <span>Magical Defense</span>
          <span className={isMagicDefChanged ? changedClassName : undefined}>
            {calculatedMagicalDefense.toLocaleString()}
          </span>
        </CardContentListItem>
        {hasHitrateStat && (
          <CardContentListItem className="flex items-center justify-between space-x-4">
            <span>Hitrate</span>
            <span className={isHitrateChanged ? changedClassName : undefined}>
              {calculatedHitrate.toLocaleString()}
            </span>
          </CardContentListItem>
        )}
        {hasAttackSpeedStat && (
          <CardContentListItem className="flex items-center justify-between space-x-4">
            <span>Attack Speed</span>
            <span
              className={isAttackSpeedChanged ? changedClassName : undefined}
            >
              {`${Math.round(calculatedAttackSpeed * 100)}%`}
            </span>
          </CardContentListItem>
        )}
        {hasPhAvoidanceStat && (
          <CardContentListItem className="flex items-center justify-between space-x-4">
            <span>Avoidance</span>
            <span
              className={hasPhAvoidanceChanged ? changedClassName : undefined}
            >
              {calculatedPhysicalAvoidance.toLocaleString()}
            </span>
          </CardContentListItem>
        )}
        {hasMovementSpeedStat && (
          <CardContentListItem className="flex items-center justify-between space-x-4">
            <span>Movement Speed</span>
            <span
              className={isMovementSpeedChanged ? changedClassName : undefined}
            >
              {`${Math.round(calculatedMovementSpeed * 100)}%`}
            </span>
          </CardContentListItem>
        )}
      </CardContentList>
    </Card>
  )
}
