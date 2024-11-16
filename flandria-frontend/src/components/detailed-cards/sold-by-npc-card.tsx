import {graphql} from "@/gql"
import {SoldByNpcFragment} from "@/gql/graphql"

import {GridItem} from "@/components/grid-item"
import {
  Card,
  CardContentLinkListItem,
  CardContentScrollList,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

graphql(`
  fragment SoldByNPC on Npc {
    code
    name
    icon
    grade
    level
    is_sea
    positions {
      map {
        name
      }
    }
  }
`)

type SoldByNPCCardProps = {
  npcs: SoldByNpcFragment[]
}

export function NPCCardItem({npc}: {npc: SoldByNpcFragment}) {
  const maps = [...new Set(npc.positions.map((posEdge) => posEdge.map.name))]

  return (
    <CardContentLinkListItem to="/database/npc/$code" params={{code: npc.code}}>
      <GridItem.NonLinkItem>
        <GridItem.Icon
          size="medium"
          variant="no-hover"
          iconName={npc.icon}
          actorGrade={npc.grade}
        />
        <GridItem.Details>
          <GridItem.Name>{npc.name}</GridItem.Name>
          <GridItem.Subs
            subs={[
              `Lv. ${npc.level}`,
              npc.is_sea ? "Sea" : "Land",
              maps.join(", "),
            ]}
          />
        </GridItem.Details>
      </GridItem.NonLinkItem>
    </CardContentLinkListItem>
  )
}

export function SoldByNPCCard({npcs: npcs}: SoldByNPCCardProps) {
  if (npcs.length === 0) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle>Sold by</CardTitle>
      </CardHeader>
      <CardContentScrollList>
        {npcs
          .sort((a, b) => b.level - a.level)
          .map((npc) => (
            <NPCCardItem npc={npc} />
          ))}
      </CardContentScrollList>
    </Card>
  )
}
