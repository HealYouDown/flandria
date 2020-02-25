import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, AvailableIn, TextCard } from "../DetailedViewComponents";

const RidingPet = ({tablename, data}) => {
  const {
    obj, random_boxes
  } = data;

  const itemInfos = [
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <Row>
      <Col md={4}>
        <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
      </Col>

      <Col md={8}>
        <TextCard title="Description" text={obj.description} />
        <AvailableIn boxes={random_boxes} />
      </Col>
    </Row>
  )
}

export default RidingPet;