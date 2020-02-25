import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, AvailableIn } from "../DetailedViewComponents";

const PetCombineHelpAndStone = ({tablename, data}) => {
  const {
    obj, dropped_by, random_boxes
  } = data;

  let itemInfos;
  if (tablename == "pet_combine_help") {
    itemInfos = [
      { label: "Value", value: `${obj.efficiency}%` },
      { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
    ]
  } else if (tablename == "pet_combine_stone") {
    itemInfos = [
      { label: "Value", value: `${obj.increment_min} ~ ${obj.increment_max}` },
      { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
    ]
  }

  return (
    <Row>
      <Col md={4}>
        <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        <AvailableIn boxes={random_boxes} />
      </Col>

      <Col md={8}>
        <DroppedBy droppedBy={dropped_by} />
      </Col>
    </Row>
  )
}

export default PetCombineHelpAndStone;