import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, BonusStats, ProducedBy, NeededFor, AvailableIn, Upgrade, DroppedBy } from "../DetailedViewComponents";

const WeaponAndArmor = ({tablename, data}) => {
  const {
    dropped_by,
    needed_for,
    obj,
    produced_by,
    random_boxes,
    upgrade_data,
  } = data;

  let itemInfos = [
    { label: "Class", value: obj.class_land },
    { label: "Level", value: `${obj.level_land}/${obj.level_sea}` },
    { label: "Tradable", value: `${obj.tradable ? "True" : "False"}` },
  ]

  if (tablename == "shield") {
    itemInfos.push({ label: "Physical Defense", value: obj.physical_defense })
    itemInfos.push({ label: "Magical Defense", value: obj.magic_defense })
  }  

  return (
    <Row>
      <Col md={4}>
        <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        <BonusStats obj={obj} />
        <ProducedBy producedBy={produced_by} />
        <NeededFor neededFor={needed_for} />
        <AvailableIn boxes={random_boxes} />
      </Col>

      <Col md={8}>
        {tablename != "shield" && (
          <Upgrade tablename={tablename} obj={obj} upgradeData={upgrade_data} />
        )}
        <DroppedBy droppedBy={dropped_by} />
      </Col>
    </Row>
  )
}

export default WeaponAndArmor;