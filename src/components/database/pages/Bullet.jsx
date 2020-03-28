import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy} from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const Bullet = ({tablename, data}) => {
  const {
    obj, dropped_by
  } = data;

  const itemInfos = [
    { label: "Buy price (500/u)", value: `${Math.round(obj.npc_price*500, 2)}` },
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        </Col>

        <Col md={8}>
          <DroppedBy droppedBy={dropped_by} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default Bullet;