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
  fragment NeededFor on RecipeProduction {
    ...ProducedBy
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
          }
        })}
      </CardContentScrollList>
    </Card>
  )
}
