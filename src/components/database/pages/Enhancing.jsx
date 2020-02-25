import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, AvailableIn, TextCard } from "../DetailedViewComponents";

const Enhancing = ({tablename, data}) => {
  const {
    obj, dropped_by, random_boxes
  } = data;

  const itemInfos = [
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
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
  )
}

export default Enhancing;