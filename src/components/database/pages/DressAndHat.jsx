import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, BonusStats, AvailableIn, ProducedBy } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const DressAndHat = ({tablename, data}) => {
  const {
    obj, dropped_by, random_boxes, produced_by,
  } = data;

  const itemInfos = [
    { label: "Class", value: obj.class_land },
    { label: "Gender", value: obj.gender },
    { label: "Level", value: `${obj.level_land}/${obj.level_sea}` },
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
          <ProducedBy producedBy={produced_by} />
          <DroppedBy droppedBy={dropped_by} />
        </Col>

        <Col md={8}>
          <BonusStats obj={obj} />
          <AvailableIn boxes={random_boxes} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default DressAndHat;