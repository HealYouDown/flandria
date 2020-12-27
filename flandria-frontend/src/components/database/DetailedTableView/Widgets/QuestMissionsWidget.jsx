import React from 'react';
import { resolveWeaponTypeToName } from '../../../../helpers';
import ListWidget, { ItemListWidgetItem, TextListWidgetItem } from './ListWidget';

function getQuestMissionContent(mission, giveItems) {
  const workType = mission.work_type.value;

  if (workType === 0) {
    // Deliver an item
    return (
      <ItemListWidgetItem
        tablename={mission.item.table}
        item={mission.item}
        subs={[`Qty. ${mission.count}x`]}
      />
    );
  }

  if ([1, 4, 17].includes(workType)) {
    // Talk to NPC, Convoy NPC, Listen to NPC
    // Also renders item(s) you may have to give to the npc
    return (
      <>
        <ItemListWidgetItem
          tablename="npc"
          item={mission.npc}
        />
        {giveItems.map((giveItem) => (
          <ItemListWidgetItem
            tablename="quest_item"
            item={giveItem.item}
            subs={[`Qty. ${giveItem.amount}x`]}
          />
        ))}
      </>
    );
  }

  if (workType === 3) {
    // Collect quest item(s)
    return (
      <ItemListWidgetItem
        tablename="quest_item"
        item={mission.quest_item}
        subs={[`Qty. ${mission.count}x`]}
      />
    );
  }

  if (workType === 2) {
    // Kill monster(s)
    return (
      <ItemListWidgetItem
        tablename="monster"
        item={mission.monster}
        subs={[`Qty. ${mission.count}x`]}
      />
    );
  }

  let text = '';

  switch (workType) {
    case 5:
      text = `Equip ${resolveWeaponTypeToName(mission.work_value)}.`;
      break;
    case 9:
      text = `Equip ${(mission.work_value === '0') ? 'Land' : 'Sea'} Skill Book.`;
      break;
    case 10:
      text = `Equip ${(mission.work_value === '0') ? 'Land' : 'Sea'} Skill Point.`;
      break;
    case 11:
      text = 'Add a Potion to your Quickslot bar.';
      break;
    case 12:
      text = 'Add a Skill to your Quickslot bar.';
      break;
    case 13:
      text = 'Build a Ship.';
      break;
    case 14:
      text = 'Tune your Ship.';
      break;
    case 15:
      text = 'Equip Sea Shells for your Ship.';
      break;
    case 16:
      text = 'Change Weapons.';
      break;
    default:
      // Some codes are excluded and should theoretically not
      // be used, but just in case, we display some ???.
      text = '???';
  }

  return (
    <TextListWidgetItem>
      {text}
    </TextListWidgetItem>
  );
}

const QuestMissionsWidget = ({ missions, missionDescriptions, giveItems }) => (
  missions.map((mission, index) => (
    <ListWidget
      key={mission.index}
      label={missionDescriptions[index]}
    >
      {getQuestMissionContent(mission, giveItems)}
    </ListWidget>
  ))
);

export default QuestMissionsWidget;
