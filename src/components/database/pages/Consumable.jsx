import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, AvailableIn, ProducedBy, NeededFor, TextCard } from "../DetailedViewComponents";

const Consumable = ({tablename, data}) => {
  const {
    obj, dropped_by, random_boxes, produced_by, needed_for
  } = data;

  const itemInfos = [
    { label: "Sell price", value: obj.npc_price_disposal },
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <Row>
      <Col md={4}>
        <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        <ProducedBy producedBy={produced_by} />
        <NeededFor neededFor={needed_for} />
        <AvailableIn boxes={random_boxes} />
      </Col>

      <Col md={8}>
        {obj.description && (
          <TextCard title="Description" text={obj.description} />
        )}
        <DroppedBy droppedBy={dropped_by} />
      </Col>
    </Row>
  )
}

export default Consumable;