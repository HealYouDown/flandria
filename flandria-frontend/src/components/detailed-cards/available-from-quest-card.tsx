import {
  QuestsCardProps,
  QuestsListCard,
} from "@/components/detailed-cards/quests-list-card"

type AvailableFromQuestCardsProps = {
  quests: QuestsCardProps["quests"]
}

export const AvailableFromQuestCards = ({
  quests,
}: AvailableFromQuestCardsProps) => (
  <QuestsListCard
    title="Available from Quests"
    renderIfEmpty={false}
    quests={quests}
  />
)
