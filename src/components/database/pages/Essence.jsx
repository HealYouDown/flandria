import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, BonusStats, ProducedBy, NeededFor, DroppedBy } from "../DetailedViewComponents";
import Ad from "../../common/Ad";
import { essenceEquipCodes } from "../../essence_equip_codes"

const Essence = ({tablename, data}) => {
  const {
    obj, produced_by, needed_for, dropped_by
  } = data;

  const itemInfos = [
    { label: "Type", value: obj.core_essence ? "Core Essence" : "Meta Essence" },
    { label: "Level", value: obj.level.toString() },
    { label: "Equip", value: essenceEquipCodes[obj.equip] },
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  return (
    <>
      <Row>
        <Col md={4}>
          <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
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

export default Essence;