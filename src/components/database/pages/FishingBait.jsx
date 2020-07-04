import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, SoldBy } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const FishingBait = ({tablename, data}) => {
  const {
    obj, sold_by
  } = data;

  const itemInfos = [
    { label: "Buy price", value: obj.npc_price },
  ]

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        </Col>
        <Col md={8}>
          <SoldBy soldBy={sold_by} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default FishingBait;