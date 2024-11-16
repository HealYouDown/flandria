import {
  booleanToDisplayString,
  characterClassStringFromObject,
  genderToString,
  shipClassFromObject,
} from "@/utils/format-helpers"
import {getLinkFromTablename} from "@/utils/utils"

import {graphql} from "@/gql"
import {Card_ItemlistItemFragment, ItemBaseFragment} from "@/gql/graphql"

import {Detail} from "@/components/detailed-cards/details-card"
import {GridItem} from "@/components/grid-item"
import {CardContentLinkListItem} from "@/components/ui/card"

import {useMemo} from "react"

graphql(`
  fragment Card_ItemlistItem on ItemList {
    code
    name
    icon
    grade
    tablename
    gender
    duration
    level_land
    level_sea
    ...CharacterClassFragment
    ...ShipClassFragment
    ...EffectsFragment
  }
`)
export type CardItemlistItem = Card_ItemlistItemFragment

type CardItemlistItemProps = {
  item: CardItemlistItem
  additionalSubs?: string[]
}
export function CardItemlistItem({
  item,
  additionalSubs = [],
}: CardItemlistItemProps) {
  const subs = useMemo(() => {
    const subs = []

    if (item.level_land !== null && item.level_sea === null) {
      subs.push(`Land Lv. ${item.level_land}`)
    } else if (item.level_land === null && item.level_sea !== null) {
      subs.push(`Sea Lv. ${item.level_sea}`)
    } else if (item.level_land !== null && item.level_sea !== null) {
      subs.push(`Lv. ${item.level_land}/${item.level_sea}`)
    }

    if (item.gender) {
      subs.push(genderToString(item.gender))
    }
    subs.push(characterClassStringFromObject(item))
    subs.push(shipClassFromObject(item))

    return [...additionalSubs, ...subs]
  }, [item, additionalSubs])

  return (
    <CardContentLinkListItem
      to={getLinkFromTablename(item.tablename)}
      params={{code: item.code}}
    >
      <GridItem.NonLinkItem>
        <GridItem.Icon
          size="medium"
          variant="no-hover"
          iconName={item.icon}
          itemGrade={item.grade}
        />
        <GridItem.Details>
          <GridItem.Name duration={item.duration}>{item.name}</GridItem.Name>
          <GridItem.Subs subs={subs} />
          <GridItem.Effects effects={item.effects || []} />
        </GridItem.Details>
      </GridItem.NonLinkItem>
    </CardContentLinkListItem>
  )
}

graphql(`
  fragment ItemBase on BaseMixin {
    code
    name
    icon
    grade
    duration
    stack_size
    npc_buy_price
    npc_sell_price
    is_tradable
    is_storageable
    is_destroyable
    is_sellable
  }
`)

export function getBaseMixinDetails(obj: ItemBaseFragment): Detail[] {
  return [
    {
      label: "Stack Size",
      description: "The maximum quantity of the item in a single stack.",
      value: obj.stack_size.toLocaleString(),
    },
    {
      label: "Tradable",
      description: "Whether the item can be traded with other players.",
      value: booleanToDisplayString(obj.is_tradable),
    },
    {
      label: "Destroyable",
      description: "Whether the item can be destroyed.",
      value: booleanToDisplayString(obj.is_destroyable),
    },
    {
      label: "Sellable",
      description: "Whether the item can be sold to NPCs.",
      value: booleanToDisplayString(obj.is_sellable),
    },
    {
      label: "Storable",
      description: "Whether the item can be stored in a private bank.",
      value: booleanToDisplayString(obj.is_storageable),
    },
    {
      label: "Buy Price",
      description: "The price to purchase the item from an NPC, if available.",
      value: `${obj.npc_buy_price.toLocaleString()} Gold`,
    },
    {
      label: "Sell Price",
      description: "The amount an NPC will pay for the item.",
      value: `${obj.npc_sell_price.toLocaleString()} Gold`,
    },
  ]
}
