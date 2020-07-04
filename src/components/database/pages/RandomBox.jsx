import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, AvailableIn, ProducedBy, NeededFor, BoxContent, SoldBy } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const RandomBox = ({tablename, data}) => {
  const {
    obj, dropped_by, random_boxes, produced_by, needed_for, sold_by
  } = data;

  const itemInfos = [
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
          <SoldBy soldBy={sold_by} />
          <AvailableIn boxes={random_boxes} />
          <DroppedBy droppedBy={dropped_by} />
          <ProducedBy producedBy={produced_by} />
          <NeededFor neededFor={needed_for} />
        </Col>

        <Col md={8}>
          <BoxContent content={obj.content} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default RandomBox;