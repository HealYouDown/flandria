import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, BonusStats, AvailableIn } from "../DetailedViewComponents";

const FishingRod = ({tablename, data}) => {
  const {
    obj, random_boxes
  } = data;

  const itemInfos = [
    { label: "Class", value: obj.class_land },
    { label: "Level", value: `${obj.level_land}/${obj.level_sea}`},
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <Row>
      <Col md={4}>
        <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
      </Col>

      <Col md={8}>
        <BonusStats obj={obj} />
        <AvailableIn boxes={random_boxes} />
      </Col>
    </Row>
  )
}

export default FishingRod;