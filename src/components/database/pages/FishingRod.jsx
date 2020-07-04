import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, BonusStats, AvailableIn, SoldBy } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const FishingRod = ({tablename, data}) => {
  const {
    obj, random_boxes, sold_by
  } = data;

  const itemInfos = [
    { label: "Class", value: obj.class_land },
    { label: "Level", value: `${obj.level_land}/${obj.level_sea}`},
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        </Col>

        <Col md={8}>
          <BonusStats obj={obj} />
          <AvailableIn boxes={random_boxes} />
          <SoldBy soldBy={sold_by} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default FishingRod;