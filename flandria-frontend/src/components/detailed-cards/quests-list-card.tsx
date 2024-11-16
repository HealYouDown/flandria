import {characterClassStringFromObject} from "@/utils/format-helpers"

import {graphql} from "@/gql"
import {QuestsList_FragmentFragment} from "@/gql/graphql"

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
  fragment QuestsList_Fragment on Quest {
    code
    title
    level
    is_sea
    is_noble
    is_saint
    is_mercenary
    is_explorer
  }
`)

export interface QuestsCardProps {
  quests: QuestsList_FragmentFragment[]
  renderIfEmpty?: boolean
  title?: string
}

export function QuestsListCard({
  quests,
  renderIfEmpty = true,
  title = "Quests",
}: QuestsCardProps) {
  if (!renderIfEmpty && quests.length === 0) return null

  let body = (
    <CardContent>
      <p>No quests found.</p>
    </CardContent>
  )
  if (quests.length > 0) {
    body = (
      <CardContentScrollList>
        {quests
          .sort((a, b) => b.level - a.level)
          .map((quest) => (
            <CardContentLinkListItem
              to="/database/quest/$code"
              params={{code: quest.code}}
            >
              <GridItem.NonLinkItem>
                <GridItem.Details>
                  <GridItem.Name>{quest.title}</GridItem.Name>
                  <GridItem.Subs
                    subs={[
                      `Lv. ${quest.level}`,
                      quest.is_sea ? "Sea" : "Land",
                      characterClassStringFromObject(quest),
                    ]}
                  />
                </GridItem.Details>
              </GridItem.NonLinkItem>
            </CardContentLinkListItem>
          ))}
      </CardContentScrollList>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
      </CardHeader>
      {body}
    </Card>
  )
}
