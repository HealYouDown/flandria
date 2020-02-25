import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, AvailableIn, ProducedBy, NeededFor, BoxContent } from "../DetailedViewComponents";

const RandomBox = ({tablename, data}) => {
  const {
    obj, dropped_by, random_boxes, produced_by, needed_for
  } = data;

  const itemInfos = [
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  console.log(obj);

  return (
    <Row>
      <Col md={4}>
        <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        <AvailableIn boxes={random_boxes} />
        <DroppedBy droppedBy={dropped_by} />
        <ProducedBy producedBy={produced_by} />
        <NeededFor neededFor={needed_for} />
      </Col>

      <Col md={8}>
        <BoxContent content={obj.content} />
      </Col>
    </Row>
  )
}

export default RandomBox;