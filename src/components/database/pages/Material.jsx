import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, AvailableIn, ProducedBy, NeededFor } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const Material = ({tablename, data}) => {
  const {
    obj, dropped_by, random_boxes, produced_by, needed_for
  } = data;

  const itemInfos = [
    { label: "Sell price", value: obj.npc_price_disposal },
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
          <DroppedBy droppedBy={dropped_by} />
          <AvailableIn boxes={random_boxes} />
        </Col>

        <Col md={8}>
          <ProducedBy producedBy={produced_by} />
          <NeededFor neededFor={needed_for} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default Material;