import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos } from "../DetailedViewComponents";

const FishingBait = ({tablename, data}) => {
  const {
    obj
  } = data;

  const itemInfos = [
    { label: "Buy price", value: obj.npc_price },
  ]

  return (
    <Row>
      <Col md={4}>
        <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
      </Col>
    </Row>
  )
}

export default FishingBait;