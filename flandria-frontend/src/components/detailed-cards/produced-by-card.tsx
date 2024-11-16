import {graphql} from "@/gql"
import {ProducedByFragment} from "@/gql/graphql"

import {GridItem} from "@/components/grid-item"
import {
  Card,
  CardContentLinkListItem,
  CardContentScrollList,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

graphql(`
  fragment ProducedBy on RecipeProduction {
    __typename
    ... on Recipe {
      code
      name
      icon
      grade
    }
    ... on Production {
      code
      result_item {
        code
        name
        icon
        grade
        duration
      }
    }
  }
`)

type ProducedByCardProps = {
  producers: ProducedByFragment[]
}

export function ProducedByCard({producers: producers}: ProducedByCardProps) {
  if (producers.length === 0) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle>Produced by</CardTitle>
      </CardHeader>
      <CardContentScrollList>
        {producers.map((producer, i) => {
          if (producer.__typename === "Recipe") {
            return (
              <CardContentLinkListItem
                key={`recipe-producer-${i}`}
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
                key={`production-producer-${i}`}
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
