import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, Quests, Drops } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const Monster = ({tablename, data}) => {
  const {
    obj, drops, quests
  } = data;

  const itemInfos = [
    { label: "Level", value: obj.level },
    { label: "Health points", value: obj.hp },
    { label: "Experience", value: obj.experience },
    { label: "Range", value: obj.range },
    { label: "Damage", value: `${obj.min_dmg} ~ ${obj.max_dmg}` },
    { label: "Physical defense", value: obj.physical_defense },
    { label: "Magical defense", value: obj.magical_defense },
  ];

  const hasQuests = quests.length >= 1;
  const dropsColWidth = hasQuests ? 4 : 8;

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        </Col>
    
        {hasQuests && (
          <Col md={4}>
            <Quests quests={quests} />
          </Col>
        )}

        <Col md={dropsColWidth}>
          <Drops drops={drops} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default Monster;