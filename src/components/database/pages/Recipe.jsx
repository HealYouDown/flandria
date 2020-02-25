import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, AvailableIn, ResultItem, MaterialList } from "../DetailedViewComponents";

const Recipe = ({tablename, data}) => {
  const {
    obj, dropped_by, random_boxes,
  } = data;

  const itemInfos = [
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <Row>
      <Col md={4}>
        <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        <DroppedBy droppedBy={dropped_by} />
        <AvailableIn boxes={random_boxes} />
      </Col>

      <Col md={8}>
        <ResultItem resultItem={obj.result_item} />
        <MaterialList materials={obj.materials} />
      </Col>
    </Row>
  )
}

export default Recipe;