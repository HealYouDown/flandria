import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, AvailableIn, ProducedBy, NeededFor } from "../DetailedViewComponents";

const FishingItem = ({tablename, data}) => {
  const {
    obj, produced_by, needed_for
  } = data;

  const itemInfos = [
    { label: "Sell price", value: obj.npc_price_disposal },
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <Row>
      <Col md={4}>
        <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
      </Col>

      <Col md={8}>
        <ProducedBy producedBy={produced_by} />
        <NeededFor neededFor={needed_for} />
      </Col>
    </Row>
  )
}

export default FishingItem;