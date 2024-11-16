import {Card_ItemlistItemFragment} from "@/gql/graphql"

import {CardItemlistItem} from "@/components/detailed-cards/helpers"
import {GridItem} from "@/components/grid-item"
import {
  Card,
  CardContentListItem,
  CardContentScrollList,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

type GenericItemlistCardProps<T> = {
  items: T[]
  itemlistGetter: (obj: T) => Card_ItemlistItemFragment
  title: string
  renderIfEmpty?: boolean
  additionalSubs?: string[]
  additionalSubsMaker?: (item: T) => string[]
}

export function GenericItemlistCard<T>({
  items,
  itemlistGetter,
  title,
  renderIfEmpty = false,
  additionalSubs = [],
  additionalSubsMaker,
}: GenericItemlistCardProps<T>) {
  if (renderIfEmpty && items.length === 0) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      <CardContentScrollList>
        {items.map((item) => {
          const itemlistItem = itemlistGetter(item)
          const subs = [
            ...additionalSubs,
            ...(additionalSubsMaker ? additionalSubsMaker(item) : []),
          ]

          if (itemlistItem.tablename === "money") {
            return (
              <CardContentListItem>
                <GridItem.NonLinkItem>
                  <GridItem.Icon
                    size="medium"
                    variant="no-hover"
                    iconName="def_004.png"
                  />
                  <GridItem.Details>
                    <GridItem.Name>Gold</GridItem.Name>
                    <GridItem.Subs subs={subs} />
                  </GridItem.Details>
                </GridItem.NonLinkItem>
              </CardContentListItem>
            )
          }

          return <CardItemlistItem item={itemlistItem} additionalSubs={subs} />
        })}
      </CardContentScrollList>
    </Card>
  )
}
