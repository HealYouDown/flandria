import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, BonusStats, AvailableIn, ProducedBy, NeededFor } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const Accessory = ({tablename, data}) => {
  const {
    obj, dropped_by, random_boxes, produced_by, needed_for
  } = data;

  const itemInfos = [
    { label: "Class", value: obj.class_land },
    { label: "Gender", value: obj.gender },
    { label: "Level", value: `${obj.level_land}/${obj.level_sea}` },
    { label: "Sell price", value: obj.npc_price_disposal },
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
          <AvailableIn boxes={random_boxes} />
          <ProducedBy producedBy={produced_by} />
          <NeededFor neededFor={needed_for} />
        </Col>

        <Col md={8}>
          <BonusStats obj={obj} />
          <DroppedBy droppedBy={dropped_by} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default Accessory;