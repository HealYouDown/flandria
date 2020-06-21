import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, TextCard } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const EssenceHelpItem = ({tablename, data}) => {
  const {
    obj, dropped_by
  } = data;

  const itemInfos = [
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        </Col>

        <Col md={8}>
          <TextCard title="Description" text={obj.description} />
          <DroppedBy droppedBy={dropped_by} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default EssenceHelpItem;