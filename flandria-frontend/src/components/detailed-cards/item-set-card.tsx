import {effectToString} from "@/utils/format-helpers"

import {graphql} from "@/gql"
import {ItemSetCardFragment} from "@/gql/graphql"

import {CardItemlistItem} from "@/components/detailed-cards/helpers"
import {
  Card,
  CardContentList,
  CardContentListItem,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

graphql(`
  fragment ItemSetCard on ItemSetMixin {
    item_set {
      name
      items {
        item {
          ...Card_ItemlistItem
        }
      }
      ...EffectsFragment
    }
  }
`)

interface ItemSetCardProps {
  itemSet: ItemSetCardFragment["item_set"]
}

export function ItemSetCard({itemSet}: ItemSetCardProps) {
  if (!itemSet) return null
  const {items, effects} = itemSet

  return (
    <Card>
      <CardHeader>
        <CardTitle>{itemSet.name}</CardTitle>
      </CardHeader>
      <CardContentList>
        {effects.map((effect) => (
          <CardContentListItem key={effect.effect_code}>
            <p>{effectToString(effect)}</p>
          </CardContentListItem>
        ))}
        {items.map((itemEdge) => (
          <CardItemlistItem key={itemEdge.item.code} item={itemEdge.item} />
        ))}
      </CardContentList>
    </Card>
  )
}
