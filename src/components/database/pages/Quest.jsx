import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, BeforeOrAfterQuest, QuestScrolls, QuestMissions, Rewards, QuestDescription } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const Quest = ({tablename, data}) => {
  const {
    obj, after_quest, quest_scrolls
  } = data;

  const itemInfos = [
    { label: "Class", value: obj.player_class },
    { label: "Level", value: obj.level },
    { label: "Location", value: (obj.location == 0 ? "Land" : "Sea") },
    { label: "EXP Reward", value: obj.exp_reward },
    { label: "Gelt Reward", value: obj.money_reward },
    { label: "Start Map", value: obj.start_map.name },
    { label: "Start NPC", value: (obj.start_npc ? obj.start_npc.name : "") },
    { label: "Finish NPC", value: obj.finish_npc.name }  
  ]

  const description = obj.descriptions.en;
  console.log(description);
  const descColWidth = (obj.missions.length >= 1 || obj.rewards.length >= 1) ? 4 : 8;

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
          
          {obj.before_quest && (
            <BeforeOrAfterQuest title="Before Quest" quest={obj.before_quest} />
          )}
          {after_quest && (
            <BeforeOrAfterQuest title="After Quest" quest={after_quest} />
          )}
          <QuestScrolls scrolls={quest_scrolls} />
        </Col>

        <Col md={4}>
          <QuestMissions missions={obj.missions} description={description} givenQuestItems={obj.given_quest_items} />
          <Rewards rewards={obj.rewards} />
        </Col>

        <Col md={descColWidth}>
          <QuestDescription title="Description" description={description.description} />
          <QuestDescription title="Pre Dialog" description={description.pre_dialog} />
          <QuestDescription title="Start Dialog" description={description.start_dialog} />
          <QuestDescription title="Run Dialog" description={description.run_dialog} />
          <QuestDescription title="Finish Dialog" description={description.finish_dialog} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default Quest;