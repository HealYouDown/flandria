import {rangeToMeters} from "@/utils/format-helpers"

import {graphql} from "@/gql"
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

graphql(`
  fragment UpgradeRule on UpgradeRule {
    level
    cost
    ...EffectsFragment
  }
`)

graphql(`
  fragment WeaponUpgradeRule on WeaponMixin {
    upgrade_rule {
      ...UpgradeRule
    }
  }
`)

interface WeaponUpgradeCard {
  upgradeRules: UpgradeRuleFragment[]
  baseMinPhDamage: number
  baseMaxPhDamage: number
  baseMinMagicDamage: number
  baseMaxMagicDamage: number
  baseAttackSpeed: number
  baseAttackRange: number
}

export function WeaponUpgradeCard({
  upgradeRules,
  baseMinPhDamage,
  baseMaxPhDamage,
  baseMinMagicDamage,
  baseMaxMagicDamage,
  baseAttackSpeed,
  baseAttackRange,
}: WeaponUpgradeCard) {
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
    calculatedMinPhDamage,
    calculatedMaxPhDamage,
    calculatedMinMagicDamage,
    calculatedMaxMagicDamage,
    calculatedAttackSpeed,
    calculatedAttackRange,
  } = React.useMemo(() => {
    let calculatedMinPhDamage = baseMinPhDamage
    let calculatedMaxPhDamage = baseMaxPhDamage
    let calculatedMinMagicDamage = baseMinMagicDamage
    let calculatedMaxMagicDamage = baseMaxMagicDamage
    const calculatedAttackSpeed = baseAttackSpeed
    const calculatedAttackRange = baseAttackRange

    currentRule.effects.forEach((effect) => {
      // Operators should be + for all weapon effects
      // Only armor has attack speed / movement speed with *
      if (effect.effect_code === EffectCode.CharMagicMinAttk) {
        calculatedMinMagicDamage = Math.floor(baseMinMagicDamage + effect.value)
      } else if (effect.effect_code === EffectCode.CharMagicMaxAttk) {
        calculatedMaxMagicDamage = Math.floor(baseMaxMagicDamage + effect.value)
      } else if (effect.effect_code === EffectCode.CharMeleeMinAttk) {
        calculatedMinPhDamage = Math.floor(baseMinPhDamage + effect.value)
      } else if (effect.effect_code === EffectCode.CharMeleeMaxAttk) {
        calculatedMaxPhDamage = Math.floor(baseMaxPhDamage + effect.value)
      } else {
        console.error(`Unknown effect code ${effect.effect_code}`)
      }
    })

    return {
      calculatedMinPhDamage,
      calculatedMaxPhDamage,
      calculatedMinMagicDamage,
      calculatedMaxMagicDamage,
      calculatedAttackSpeed,
      calculatedAttackRange,
    }
  }, [
    currentRule,
    baseMinPhDamage,
    baseMaxPhDamage,
    baseMinMagicDamage,
    baseMaxMagicDamage,
    baseAttackSpeed,
    baseAttackRange,
  ])

  const changedClassName = "text-green-600 dark:text-green-400"
  const isPhDamageChanged =
    baseMinPhDamage !== calculatedMinPhDamage ||
    baseMaxPhDamage !== calculatedMaxPhDamage
  const isMagicDamageChanged =
    baseMinMagicDamage !== calculatedMinMagicDamage ||
    baseMaxMagicDamage !== calculatedMaxMagicDamage
  const isAttackSpeedChanged = baseAttackSpeed !== calculatedAttackSpeed
  const isAttackRangeChanged = baseAttackRange !== calculatedAttackRange

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
          <span>Physical Damage</span>
          <span
            className={isPhDamageChanged ? changedClassName : undefined}
          >{`${calculatedMinPhDamage.toLocaleString()} ~ ${calculatedMaxPhDamage.toLocaleString()}`}</span>
        </CardContentListItem>
        <CardContentListItem className="flex items-center justify-between space-x-4">
          <span>Magical Damage</span>
          <span
            className={isMagicDamageChanged ? changedClassName : undefined}
          >{`${calculatedMinMagicDamage.toLocaleString()} ~ ${calculatedMaxMagicDamage.toLocaleString()}`}</span>
        </CardContentListItem>
        <CardContentListItem className="flex items-center justify-between space-x-4">
          <span>Attack Speed</span>
          <span className={isAttackSpeedChanged ? changedClassName : undefined}>
            {`${calculatedAttackSpeed}s`}
          </span>
        </CardContentListItem>
        <CardContentListItem className="flex items-center justify-between space-x-4">
          <span>Attack Range</span>
          <span className={isAttackRangeChanged ? changedClassName : undefined}>
            {`${rangeToMeters(calculatedAttackRange)}m`}
          </span>
        </CardContentListItem>
      </CardContentList>
    </Card>
  )
}
