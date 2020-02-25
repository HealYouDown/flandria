import React from "react";
import { Row, Col } from "react-grid-system";
import { Infos, DroppedBy, AvailableIn, ProducedBy, NeededFor } from "../DetailedViewComponents";

const ShipStuff = ({tablename, data}) => {
  const {
    obj, dropped_by, random_boxes, produced_by, needed_for,
  } = data;


    // Item Infos
  let itemInfos = [
    { label: "Buy price", value: obj.npc_price },
    { label: "Sell price", value: obj.npc_price_disposal },
    { label: "Tuning price", value: obj.npc_price_tuning },
  ];

  if (tablename == "ship_anchor") {
    itemInfos.unshift(
      { label: "Class", value: obj.class_sea },
      { label: "Level", value: obj.level_sea },
      { label: "Ship deceleration", value: obj.ship_deceleration },
      { label: "Ship turnpower", value: obj.ship_turnpower },
    )
  }

  else if (tablename == "ship_body") {
    itemInfos.unshift(
      { label: "Class", value: obj.class_sea },
      { label: "Level", value: obj.level_sea },
      { label: "Phyiscal defense", value: obj.physical_defense },
      { label: "Protection", value: obj.protection },
      { label: "DP", value: obj.ability_hp },
    )
  }

  else if (tablename == "ship_figure") {
    itemInfos.unshift(
      { label: "Class", value: obj.class_sea },
      { label: "Level", value: obj.level_sea },
      { label: "Protection", value: obj.protection },
      { label: "Balance", value: obj.balance },
    )
  }

  else if (tablename == "ship_head_mast") {
    itemInfos.unshift(
      { label: "Class", value: obj.class_sea },
      { label: "Level", value: obj.level_sea },
      { label: "Ship wind favorable", value: obj.ship_wind_favorable },
      { label: "Ship wind adverse", value: obj.ship_wind_adverse },
      { label: "Ship turnpower", value: obj.ship_turnpower },
    )
  }

  else if (tablename == "ship_main_mast") {
    itemInfos.unshift(
      { label: "Class", value: obj.class_sea },
      { label: "Level", value: obj.level_sea },
      { label: "Ship wind favorable", value: obj.ship_wind_favorable },
      { label: "Ship wind adverse", value: obj.ship_wind_adverse },
      { label: "Ship acceleration", value: obj.ship_acceleration },
      { label: "Ship deceleration", value: obj.ship_deceleration },
      { label: "Ship turnpower", value: obj.ship_turnpower },
    )
  }

  else if (tablename == "ship_magic_stone") {
    itemInfos.unshift(
      { label: "Class", value: obj.class_sea },
      { label: "Level", value: obj.level_sea },
      { label: "EN", value: obj.ability_en },
      { label: "EN recovery", value: obj.ability_en_recovery },
    )
  }

  else if (tablename == "ship_front") {
    itemInfos.unshift(
      { label: "Class", value: obj.class_sea },
      { label: "Level", value: obj.level_sea },
      { label: "Physical defence", value: obj.physical_defense },
      { label: "Protection", value: obj.protection },
      { label: "DP", value: obj.ability_hp },
      { label: "Balance", value: obj.balance },
    )
  }

  else if (tablename == "ship_normal_weapon") {
    itemInfos.unshift(
      { label: "Class", value: obj.class_sea },
      { label: "Level", value: obj.level_sea },
      { label: "Damage", value: obj.ship_defense },
      { label: "Critical", value: obj.critical },
      { label: "Cannon range", value: `${obj.ship_range/10}m` },
      { label: "Reloadspeed", value: obj.ship_reloadspeed },
      { label: "Guns range", value: `${obj.ship_hitrange/10}m` },
    )
  }

  else if (tablename == "ship_special_weapon") {
    itemInfos.unshift(
      { label: "Class", value: obj.class_sea },
      { label: "Level", value: obj.level_sea },
      { label: "Damage", value: obj.ship_defense },
      { label: "Critical", value: obj.critical },
      { label: "Range", value: `${obj.ship_range/10}m` },
      { label: "Reloadspeed", value: obj.ship_reloadspeed },
      { label: "EN usage", value: obj.ability_en_usage },
    )
  }

  return (
    <Row>
      <Col md={4}>
        <Infos tablename={tablename} data={obj} itemInfos={itemInfos} />
        <AvailableIn boxes={random_boxes} />
      </Col>

      <Col md={8}>
        <DroppedBy droppedBy={dropped_by} />
        <ProducedBy producedBy={produced_by} />
        <NeededFor neededFor={needed_for} />
      </Col>
    </Row>
  )
}

export default ShipStuff;