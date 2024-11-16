import {graphql} from "@/gql"
import {
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

graphql(`
  fragment DropsList_Fragment on Drop {
    quantity
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

        {drops.sort(sortDrops).map((drop) => {
          const {quantity, item} = drop
          const additionalSubs = quantity > 1 ? [`Qty. ${quantity}x`] : []
          return (
            <CardItemlistItem item={item} additionalSubs={additionalSubs} />
          )
        })}
      </CardContentScrollList>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Drops</CardTitle>
      </CardHeader>
      {body}
    </Card>
  )
}
