import {graphql} from "@/gql"
import {NeededForFragment} from "@/gql/graphql"

import {GridItem} from "@/components/grid-item"
import {
  Card,
  CardContentLinkListItem,
  CardContentScrollList,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

graphql(`
  fragment NeededFor on NeededFor {
    __typename
    ...ProducedBy
    ... on NpcExchangeItem {
      gelt
      item {
        code
        name
        icon
        grade
        duration
      }
      npc {
        code
        name
      }
      materials {
        quantity
        item {
          name
        }
      }
    }
  }
`)

type NeededForCardProps = {
  consumers: NeededForFragment[]
}

export function NeededForCard({consumers}: NeededForCardProps) {
  if (consumers.length === 0) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle>Needed by</CardTitle>
      </CardHeader>
      <CardContentScrollList>
        {consumers.map((producer, i) => {
          if (producer.__typename === "Recipe") {
            return (
              <CardContentLinkListItem
                key={`recipe-consumers-${i}`}
                to="/database/recipe/$code"
                params={{code: producer.code}}
              >
                <GridItem.NonLinkItem>
                  <GridItem.Icon
                    size="medium"
                    variant="no-hover"
                    iconName={producer.icon}
                    itemGrade={producer.grade}
                  />
                  <GridItem.Details>
                    <GridItem.Name>{producer.name}</GridItem.Name>
                  </GridItem.Details>
                </GridItem.NonLinkItem>
              </CardContentLinkListItem>
            )
          } else if (producer.__typename === "Production") {
            const {result_item} = producer
            return (
              <CardContentLinkListItem
                key={`production-consumers-${i}`}
                to="/database/production/$code"
                params={{code: producer.code}}
              >
                <GridItem.NonLinkItem>
                  <GridItem.Icon
                    size="medium"
                    variant="no-hover"
                    iconName={result_item.icon}
                    itemGrade={result_item.grade}
                  />
                  <GridItem.Details>
                    <GridItem.Name duration={result_item.duration}>
                      {result_item.name}
                    </GridItem.Name>
                  </GridItem.Details>
                </GridItem.NonLinkItem>
              </CardContentLinkListItem>
            )
          } else if (producer.__typename === "NpcExchangeItem") {
            const {item, npc} = producer
            const costs = producer.materials.map(
              (m) => `${m.quantity.toLocaleString()}x ${m.item.name}`,
            )
            if (producer.gelt > 0) {
              costs.push(`${producer.gelt.toLocaleString()} Gelt`)
            }
            return (
              <CardContentLinkListItem
                key={`exchange-consumers-${i}`}
                to="/database/npc/$code"
                params={{code: npc.code}}
              >
                <GridItem.NonLinkItem>
                  <GridItem.Icon
                    size="medium"
                    variant="no-hover"
                    iconName={item.icon}
                    itemGrade={item.grade}
                  />
                  <GridItem.Details>
                    <GridItem.Name duration={item.duration}>
                      {item.name}
                    </GridItem.Name>
                    <GridItem.Subs
                      subs={[`Exchange at ${npc.name}`, costs.join(", ")]}
                    />
                  </GridItem.Details>
                </GridItem.NonLinkItem>
              </CardContentLinkListItem>
            )
          }
        })}
      </CardContentScrollList>
    </Card>
  )
}
