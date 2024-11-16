import {uniqueBy} from "@/utils/utils"

import {graphql} from "@/gql"
import {RandomBoxFragment} from "@/gql/graphql"

import {GridItem} from "@/components/grid-item"
import {
  Card,
  CardContentLinkListItem,
  CardContentScrollList,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

graphql(`
  fragment RandomBox on RandomBox {
    code
    name
    icon
    grade
    level_land
    level_sea
  }
`)

type AvailableInRandomboxCardProps = {
  boxes: RandomBoxFragment[]
}

export function AvailableInRandomboxCard({
  boxes,
}: AvailableInRandomboxCardProps) {
  if (boxes.length === 0) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle>Available in</CardTitle>
      </CardHeader>
      <CardContentScrollList>
        {uniqueBy({array: boxes, keyFn: (box) => box.code}).map((box) => (
          <CardContentLinkListItem
            key={box.code}
            to="/database/random_box/$code"
            params={{code: box.code}}
          >
            <GridItem.NonLinkItem>
              <GridItem.Icon
                size="medium"
                variant="no-hover"
                iconName={box.icon}
                itemGrade={box.grade}
              />
              <GridItem.Details>
                <GridItem.Name>{box.name}</GridItem.Name>
                <GridItem.Subs
                  subs={[`Lv. ${box.level_land}/${box.level_sea}`]}
                />
              </GridItem.Details>
            </GridItem.NonLinkItem>
          </CardContentLinkListItem>
        ))}
      </CardContentScrollList>
    </Card>
  )
}
