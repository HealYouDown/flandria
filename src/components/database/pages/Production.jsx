import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, ResultItem, MaterialList } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const Production = ({tablename, data}) => {
  const {
    obj, premium_essence_recipe,
  } = data;

  const itemInfos = [
    { label: "Type", value: obj.type },
    { label: "Required points", value: obj.points_needed },
  ]

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        </Col>

        <Col md={8}>
          <ResultItem resultItem={obj.result_item} />
          <MaterialList materials={obj.materials} />
          {premium_essence_recipe && (
            <MaterialList title="Materials Premium" materials={premium_essence_recipe.materials} />
          )}
        </Col>

      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default Production;