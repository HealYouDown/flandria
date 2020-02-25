import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, ResultItem, MaterialList } from "../DetailedViewComponents";

const Recipe = ({tablename, data}) => {
  const {
    obj
  } = data;

  const itemInfos = [
    { label: "Type", value: obj.production.type },
    { label: "Required points", value: obj.production.points_needed },
  ]

  return (
    <Row>
      <Col md={4}>
        <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
      </Col>

      <Col md={8}>
        <ResultItem resultItem={obj.production.result_item} />
        <MaterialList materials={obj.production.materials} />
      </Col>
    </Row>
  )
}

export default Recipe;