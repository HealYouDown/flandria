import {graphql} from "@/gql"
import {QuestRewardEdgeFragment} from "@/gql/graphql"

import {CardItemlistItem} from "@/components/detailed-cards/helpers"
import {
  Card,
  CardContentScrollList,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

graphql(`
  fragment QuestRewardEdge on QuestRewardItem {
    amount
    item {
      ...Card_ItemlistItem
    }
  }
`)

type QuestRewardsCardProps = {
  rewards: QuestRewardEdgeFragment[]
  selectableCount: number
}

export function QuestRewardsCard({
  rewards,
  selectableCount,
}: QuestRewardsCardProps) {
  if (rewards.length === 0) return null

  return (
    <Card>
      <CardHeader>
        <CardTitle>Rewards</CardTitle>
        <CardDescription>
          Select {selectableCount}/{rewards.length}
        </CardDescription>
      </CardHeader>
      <CardContentScrollList>
        {rewards.map((edge) => {
          const {amount, item} = edge
          const additionalSubs = amount > 1 ? [`Qty. ${amount}x`] : []
          return (
            <CardItemlistItem item={item} additionalSubs={additionalSubs} />
          )
        })}
      </CardContentScrollList>
    </Card>
  )
}
