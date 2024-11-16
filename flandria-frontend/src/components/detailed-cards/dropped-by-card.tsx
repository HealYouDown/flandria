import {monsterGradeToString} from "@/utils/format-helpers"
import {uniqueBy} from "@/utils/utils"

import {graphql} from "@/gql"
import {ActorGrade, DroppedByFragment} from "@/gql/graphql"

import {GridItem} from "@/components/grid-item"
import {
  Card,
  CardContent,
  CardContentLinkListItem,
  CardContentScrollList,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

graphql(`
  fragment DroppedBy on Drop {
    monster {
      code
      name
      icon
      grade
      level
      is_sea
    }
  }
`)

type Drop = DroppedByFragment

const actorGradeSortBoost = {
  [ActorGrade.Normal]: 1,
  [ActorGrade.Elite]: 2,
  [ActorGrade.MiniBoss]: 3,
  [ActorGrade.Boss]: 4,
}

function sortDrops(a: Drop, b: Drop): number {
  const rarityValueA = actorGradeSortBoost[a.monster.grade]
  const rarityValueB = actorGradeSortBoost[b.monster.grade]

  // First sort by rarity
  if (rarityValueA > rarityValueB) return -1
  if (rarityValueA < rarityValueB) return 1

  // Theb by level
  if (a.monster.level > b.monster.level) return -1
  if (a.monster.level < b.monster.level) return 1

  // If they are the same, sort by name
  if (a.monster.name > b.monster.name) return 1
  if (a.monster.name < b.monster.name) return -1

  return 1
}

type DroppedByCardProps = {
  droppedBy: Drop[]
}

export function DroppedByCard({droppedBy}: DroppedByCardProps) {
  let body = (
    <CardContent>
      <p>No monsters found</p>
    </CardContent>
  )

  if (droppedBy.length > 0) {
    body = (
      <CardContentScrollList>
        {uniqueBy({array: droppedBy, keyFn: (a) => a.monster.code})
          .sort(sortDrops)
          .map((dropEdge) => {
            const {monster} = dropEdge
            return (
              <CardContentLinkListItem
                key={dropEdge.monster.code}
                to="/database/monster/$code"
                params={{code: monster.code}}
              >
                <GridItem.NonLinkItem>
                  <GridItem.Icon
                    size="medium"
                    variant="no-hover"
                    iconName={monster.icon}
                    actorGrade={monster.grade}
                  />
                  <GridItem.Details>
                    <GridItem.Name>{monster.name}</GridItem.Name>
                    <GridItem.Subs
                      subs={[
                        `Lv. ${monster.level}`,
                        monsterGradeToString(monster.grade),
                        monster.is_sea ? "Sea" : "Land",
                      ]}
                    />
                  </GridItem.Details>
                </GridItem.NonLinkItem>
              </CardContentLinkListItem>
            )
          })}
      </CardContentScrollList>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Dropped by</CardTitle>
      </CardHeader>
      {body}
    </Card>
  )
}
