import {formatPercent} from "@/lib/utils"

import {graphql} from "@/gql"
import {
  DropDistribution,
  DropsListMoney_FragmentFragment,
  DropsList_FragmentFragment,
} from "@/gql/graphql"

import {CardItemlistItem} from "@/components/detailed-cards/helpers"
import {GridItem} from "@/components/grid-item"
import {
  Card,
  CardContent,
  CardContentListItem,
  CardContentScrollList,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import React from "react"

graphql(`
  fragment DropsList_Fragment on Drop {
    quantity
    section_id
    section_probability
    section_guaranteed
    item_probability
    distribution
    max_per_player
    bypass_level
    item {
      ...Card_ItemlistItem
    }
  }
`)

graphql(`
  fragment DropsListMoney_Fragment on Money {
    min
    max
  }
`)

type Drop = DropsList_FragmentFragment
type Money = DropsListMoney_FragmentFragment

const tablenamePriority = {
  essence: 11000,
  essence_help: 10500,
  material: 10000,
  upgrade_help: 9950,
  seal_break_help: 9949,
  seal_extend: 9948,
  pet_skill_stone: 9900,
  random_box: 9800,
  cariad: 1000,
  rapier: 999,
  dagger: 998,
  one_handed_sword: 997,
  two_handed_sword: 996,
  rifle: 995,
  duals: 994,
  shield: 993,
  hat: 800,
  dress: 799,
  accessory: 798,
  coat: 550,
  pants: 549,
  shoes: 548,
  gauntlet: 547,
  consumable: 300,
  upgrade_stone: 250,
  pet_combine_help: 200,
  pet_combine_stone: 199,
  ship_normal_weapon: 152,
  ship_special_weapon: 151,
  ship_body: 150,
  ship_front: 149,
  ship_head_mast: 148,
  ship_main_mast: 147,
  ship_figure: 146,
  ship_magic_stone: 145,
  ship_anchor: 144,
  ship_flag: 143,
  recipe: 100,
  quest_scroll: 99,
  quest_item: 98,
  bullet: 2,
  ship_shell: 1,
}

function sortDrops(a: Drop, b: Drop): number {
  const valA =
    tablenamePriority[a.item.tablename as keyof typeof tablenamePriority] || 0
  const valB =
    tablenamePriority[b.item.tablename as keyof typeof tablenamePriority] || 0

  // First sort by table value
  if (valA > valB) return -1
  if (valA < valB) return 1

  // If they are the same, sort by name
  if (a.item.name > b.item.name) return 1
  if (a.item.name < b.item.name) return -1

  return 1
}

function dropRuleSubs(drop: Drop): string[] {
  const subs = []
  if (drop.distribution === DropDistribution.PerPlayer) {
    subs.push("Every party member")
  } else if (drop.distribution === DropDistribution.Shared) {
    subs.push(
      drop.max_per_player
        ? `Split in party (max. ${drop.max_per_player} each)`
        : "Split in party",
    )
  }
  if (drop.bypass_level) {
    subs.push("No level restriction")
  }
  return subs
}

interface DropsCardProps {
  money?: Money | null
  drops: Drop[]
}

export function DropsListCard({money, drops}: DropsCardProps) {
  let body = (
    <CardContent>
      <p>No drops found.</p>
    </CardContent>
  )

  // Groups drops by their category, in the order of the drop file
  const sections = React.useMemo(() => {
    const map = new Map<number, Drop[]>()
    for (const drop of [...drops].sort((a, b) => a.section_id - b.section_id)) {
      if (!map.has(drop.section_id)) map.set(drop.section_id, [])
      map.get(drop.section_id)!.push(drop)
    }
    return [...map.values()].map((sectionDrops) => sectionDrops.sort(sortDrops))
  }, [drops])

  if (drops.length > 0 || !!money) {
    body = (
      <CardContentScrollList>
        {money && (
          <CardContentListItem>
            <GridItem.NonLinkItem>
              <GridItem.Icon
                size="medium"
                variant="no-hover"
                iconName="def_004.png"
              />
              <GridItem.Details>
                <GridItem.Name>Gold</GridItem.Name>
                <GridItem.Subs
                  subs={[
                    `${money.min.toLocaleString()} ~ ${money.max.toLocaleString()}`,
                  ]}
                />
              </GridItem.Details>
            </GridItem.NonLinkItem>
          </CardContentListItem>
        )}

        {sections.map((sectionDrops, sectionIdx) => {
          const first = sectionDrops[0]
          const sectionChance = first.section_guaranteed
            ? "Always drops all items"
            : `${formatPercent(first.section_probability)} chance to roll`

          return (
            <React.Fragment key={first.section_id}>
              <CardContentListItem className="bg-muted/50 py-1.5">
                <div className="flex items-baseline justify-between gap-2 text-sm">
                  <span className="font-semibold tracking-tight">
                    Category {String.fromCharCode(65 + sectionIdx)}
                  </span>
                  <span className="text-xs text-foreground/70">
                    {sectionChance}
                  </span>
                </div>
              </CardContentListItem>
              {sectionDrops.map((drop, idx) => {
                const {quantity, item} = drop
                const subs = []
                if (!drop.section_guaranteed) {
                  subs.push(
                    `Chance: ${formatPercent(drop.section_probability * drop.item_probability)}`,
                  )
                }
                if (quantity > 1) {
                  subs.push(`Qty. ${quantity}x`)
                }
                subs.push(...dropRuleSubs(drop))
                return (
                  <CardItemlistItem
                    key={`${item.code}-${idx}`}
                    item={item}
                    additionalSubs={subs}
                  />
                )
              })}
            </React.Fragment>
          )
        })}
      </CardContentScrollList>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Drops</CardTitle>
        <p className="text-xs leading-tight text-foreground/70">
          Drops are organized into categories. Each category has a chance to
          roll. If it does, exactly one item from that category is chosen based
          on its individual chance. Some categories always drop all of their
          items.
          <br />
          The chances shown per item reflect the final probability. In a party,
          some items go to every member or are split between them. Only members
          at most 9 levels below the monster receive them, unless marked with no
          level restriction.
        </p>
      </CardHeader>
      {body}
    </Card>
  )
}
