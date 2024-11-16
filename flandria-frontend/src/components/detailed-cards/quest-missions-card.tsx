import {monsterGradeToString} from "@/utils/format-helpers"

import {graphql} from "@/gql"
import {
  QuestGiveItemFragment,
  QuestMissionFragment,
  QuestMissionType,
} from "@/gql/graphql"

import {CardItemlistItem} from "@/components/detailed-cards/helpers"
import {NPCCardItem} from "@/components/detailed-cards/sold-by-npc-card"
import {GridItem} from "@/components/grid-item"
import {
  Card,
  CardContent,
  CardContentLinkListItem,
  CardContentList,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

graphql(`
  fragment QuestMission on QuestMission {
    work_type
    count
    description

    item {
      ...Card_ItemlistItem
    }

    monster {
      code
      name
      icon
      grade
      level
      is_sea
    }

    quest_item {
      code
      name
      icon
      grade
    }

    map {
      code
      name
    }

    npc {
      ...SoldByNPC
    }
  }
`)

graphql(`
  fragment QuestGiveItem on QuestGiveItem {
    amount
    item {
      ...Card_ItemlistItem
    }
  }
`)

graphql(`
  fragment QuestMissions on Quest {
    missions {
      ...QuestMission
    }
    give_items {
      ...QuestGiveItem
    }
  }
`)

interface QuestMissionsCardProps {
  missions: QuestMissionFragment[]
  giveItems: QuestGiveItemFragment[]
}

// Actually used:
//        KILL_MONSTER               2
//        COLLECT_QUEST_ITEM         3
//        TALK_TO_NPC                1
//        PROTECT_NPC                4
//        EQUIP_ITEM                 5
//        CHANGE_WEAPONS             16
//      USE_STATPOINT              8
//      USE_SKILLBOOK              9
//      USE_SKILLPOINT             10
//        ADD_SKILL_TO_SLOT_BAR      12
//      ADD_CONSUMABLE_TO_SLOT_BAR 11
//        REGISTER_SHIP              13
//      TUNE_SHIP                  14
//        EQUIP_SEA_SHELLS           15
//          DELIVER_ITEM               0
// UNSEAL_ITEM                18

export function QuestMissionsCard({
  missions,
  giveItems,
}: QuestMissionsCardProps) {
  return missions.map((mission) => {
    let body

    if (mission.work_type === QuestMissionType.DeliverItem && mission.item) {
      body = (
        <CardContentList>
          <CardItemlistItem item={mission.item} />
        </CardContentList>
      )
    } else if (
      (mission.work_type === QuestMissionType.TalkToNpc ||
        mission.work_type === QuestMissionType.ProtectNpc ||
        mission.work_type === QuestMissionType.ListenToNpc) &&
      mission.npc
    ) {
      body = (
        <CardContentList>
          <NPCCardItem npc={mission.npc} />
          {giveItems.map((itemEdge) => (
            <CardItemlistItem
              item={itemEdge.item}
              additionalSubs={[`Qty. ${itemEdge.amount}x`]}
            />
          ))}
        </CardContentList>
      )
    } else if (
      mission.work_type === QuestMissionType.CollectQuestItem &&
      mission.quest_item
    ) {
      const questItem = mission.quest_item
      body = (
        <CardContentList>
          <CardContentLinkListItem
            to="/database/quest_item/$code"
            params={{code: questItem.code}}
          >
            <GridItem.NonLinkItem>
              <GridItem.Icon iconName={questItem.icon} variant="no-hover" />
              <GridItem.Details>
                <GridItem.Name>{questItem.name}</GridItem.Name>
                <GridItem.Subs subs={[`Qty. ${mission.count}x`]} />
              </GridItem.Details>
            </GridItem.NonLinkItem>
          </CardContentLinkListItem>
        </CardContentList>
      )
    } else if (
      mission.work_type === QuestMissionType.KillMonster &&
      mission.monster
    ) {
      const monster = mission.monster
      body = (
        <CardContentList>
          <CardContentLinkListItem
            to="/database/monster/$code"
            params={{code: monster.code}}
          >
            <GridItem.NonLinkItem>
              <GridItem.Icon iconName={monster.icon} variant="no-hover" />
              <GridItem.Details>
                <GridItem.Name>{monster.name}</GridItem.Name>
                <GridItem.Subs
                  subs={[
                    `Qty. ${mission.count}x`,
                    `Lv. ${monster.level}`,
                    monsterGradeToString(monster.grade),
                    monster.is_sea ? "Sea" : "Land",
                  ]}
                />
              </GridItem.Details>
            </GridItem.NonLinkItem>
          </CardContentLinkListItem>
        </CardContentList>
      )
    } else if (
      mission.work_type === QuestMissionType.EquipItem ||
      mission.work_type === QuestMissionType.UseSkillbook ||
      mission.work_type === QuestMissionType.UseSkillpoint ||
      mission.work_type === QuestMissionType.AddConsumableToSlotBar ||
      mission.work_type === QuestMissionType.AddSkillToSlotBar ||
      mission.work_type === QuestMissionType.RegisterShip ||
      mission.work_type === QuestMissionType.TuneShip ||
      mission.work_type === QuestMissionType.EquipSeaShells ||
      mission.work_type === QuestMissionType.ChangeWeapons ||
      mission.work_type === QuestMissionType.UnsealItem
    ) {
      const text = {
        [QuestMissionType.EquipItem]: "Equip the item.",
        [QuestMissionType.UseSkillbook]: "Use a skill book.",
        [QuestMissionType.UseSkillpoint]: "Use a skill point.",
        [QuestMissionType.AddConsumableToSlotBar]:
          "Add a potion to your quickslot bar.",
        [QuestMissionType.AddSkillToSlotBar]:
          "Add a skill to your quickslot bar.",
        [QuestMissionType.RegisterShip]: "Build a ship.",
        [QuestMissionType.TuneShip]: "Upgrade your ship.",
        [QuestMissionType.EquipSeaShells]: "Equip sea shells.",
        [QuestMissionType.ChangeWeapons]: "Change your weapons.",
        [QuestMissionType.UnsealItem]: "Unseal an item.",
      }[mission.work_type]
      return (
        <CardContent>
          <p>{text}</p>
        </CardContent>
      )
    } else {
      console.error("Unknown mission type", mission.work_type, mission)
      body = null
    }

    return (
      <Card>
        <CardHeader>
          <CardTitle>{mission.description}</CardTitle>
        </CardHeader>
        {body}
      </Card>
    )
  })
}
