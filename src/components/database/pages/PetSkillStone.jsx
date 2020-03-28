import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, AvailableIn, TextCard } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const PetSkillStone = ({tablename, data}) => {
  const {
    obj, dropped_by, random_boxes
  } = data;

  const itemInfos = [
    { label: "Level", value: obj.level },
    { label: "Cooldown", value: `${obj.cooldown/1000}s` },
    { label: "Casttime", value: `${obj.casttime/1000}s` },
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
          <AvailableIn boxes={random_boxes} />
        </Col>

        <Col md={8}>
          <TextCard title="Description" text={obj.description} />
          <DroppedBy droppedBy={dropped_by} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default PetSkillStone;