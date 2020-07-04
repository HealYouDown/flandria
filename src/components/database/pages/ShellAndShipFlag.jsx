import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, AvailableIn, ProducedBy, NeededFor, SoldBy } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const ShellAndShipFlag = ({tablename, data}) => {
  const {
    obj, dropped_by, sold_by,
  } = data;

  let itemInfos;
  if (tablename == "shell") {
    itemInfos = [
      { label: "Level", value: obj.level_sea },
      { label: "Damage", value: obj.damage },
    ]
  }
  else if (tablename == "ship_flag") {
    itemInfos = [
      { label: "Level", value: obj.level_sea },
      { label: "Buy price", value: obj.npc_price },
      { label: "Sell price", value: obj.npc_price_disposal },
      { label: "Tuning price", value: obj.npc_price_tuning },
    ]
  }

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        </Col>

        <Col md={8}>
          <DroppedBy droppedBy={dropped_by} />
          <SoldBy soldBy={sold_by} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default ShellAndShipFlag;