import {formatSeconds} from "@/utils/date-helpers"
import {rangeToMeters} from "@/utils/format-helpers"

import {graphql} from "@/gql"
import {ShipDetailsFragment} from "@/gql/graphql"

import {Detail, DetailsCard} from "@/components/detailed-cards/details-card"

import * as React from "react"

graphql(`
  fragment ShipDetails on ShipBaseMixin {
    guns_front
    guns_side
    crew_size
    physical_defense
    protection
    balance
    dp
    en
    en_usage
    en_recovery
    acceleration
    deceleration
    turning_power
    favorable_wind
    adverse_wind
    physical_damage
    weapon_range
    critical_chance
    reload_speed
    hit_range
  }
`)

type ShipDetailsCardProps = {
  item: ShipDetailsFragment
}

export function ShipDetailsCard({item}: ShipDetailsCardProps) {
  const details = React.useMemo<Detail[]>(() => {
    const details: Detail[] = []

    if (item.guns_front > 0) {
      details.push({
        label: "Guns front",
        value: item.guns_front.toLocaleString(),
      })
    }
    if (item.guns_side > 0) {
      details.push({
        label: "Guns side",
        value: item.guns_side.toLocaleString(),
      })
    }
    if (item.crew_size > 0) {
      details.push({
        label: "Crew size",
        value: item.crew_size.toLocaleString(),
      })
    }
    if (item.physical_defense > 0) {
      details.push({
        label: "Physical defense",
        value: item.physical_defense.toLocaleString(),
      })
    }
    if (item.protection > 0) {
      details.push({
        label: "Protection",
        value: item.protection.toLocaleString(),
      })
    }
    if (item.balance > 0) {
      details.push({
        label: "Balance",
        value: item.balance.toLocaleString(),
      })
    }
    if (item.dp > 0) {
      details.push({
        label: "DP",
        value: item.dp.toLocaleString(),
      })
    }
    if (item.en > 0) {
      details.push({
        label: "EN",
        value: item.en.toLocaleString(),
      })
    }
    if (item.en_usage > 0) {
      details.push({
        label: "EN usage",
        value: item.en_usage.toLocaleString(),
      })
    }
    if (item.en_recovery > 0) {
      details.push({
        label: "EN recovery",
        value: item.en_recovery.toLocaleString(),
      })
    }
    if (item.acceleration > 0) {
      details.push({
        label: "Acceleration",
        value: item.acceleration.toLocaleString(),
      })
    }
    if (item.deceleration > 0) {
      details.push({
        label: "Deceleration",
        value: item.deceleration.toLocaleString(),
      })
    }
    if (item.turning_power > 0) {
      details.push({
        label: "Turning power",
        value: item.turning_power.toLocaleString(),
      })
    }
    if (item.favorable_wind > 0) {
      details.push({
        label: "Favorable wind",
        value: item.favorable_wind.toLocaleString(),
      })
    }
    if (item.adverse_wind > 0) {
      details.push({
        label: "Adverse wind",
        value: item.adverse_wind.toLocaleString(),
      })
    }
    if (item.physical_damage > 0) {
      details.push({
        label: "Physical damage",
        value: item.physical_damage.toLocaleString(),
      })
    }
    if (item.weapon_range > 0) {
      details.push({
        label: "Weapon range",
        value: `${rangeToMeters(item.weapon_range, 10)}m`,
      })
    }
    if (item.critical_chance > 0) {
      details.push({
        label: "Critical chance",
        value: `${Math.round(item.critical_chance * 100)}%`,
      })
    }
    if (item.reload_speed > 0) {
      details.push({
        label: "Reload speed",
        value: formatSeconds(item.reload_speed),
      })
    }
    if (item.hit_range > 0) {
      details.push({
        label: "Hit range",
        value: `${rangeToMeters(item.hit_range, 10)}m`,
      })
    }

    return details
  }, [item])

  return <DetailsCard title="Ship Stats" details={details} />
}
