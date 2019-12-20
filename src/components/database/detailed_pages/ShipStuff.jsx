import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import AvailableIn from "../detailed_pages_components/AvailableIn";
import DroppedBy from "../detailed_pages_components/DroppedBy";
import Infos from "../detailed_pages_components/Infos";
import NeededFor from "../detailed_pages_components/NeededFor";
import ProducedBy from "../detailed_pages_components/ProducedBy";
import LoadingScreen from "../../layout/LoadingScreen";

export default class ShipStuff extends React.Component {
  constructor(props) {
    super(props);
    this.table = this.props.table;
    this.code = this.props.match.params.code;

    this.state = {
      loading: true,
      data: {},
      error: false,
      errorMessage: "",
    }
  }

  componentDidMount() {
    fetchDetailedPageData(this.table, this.code, this.setState.bind(this));
  }

  render() {
    const {
      loading,
      data,
      error,
      errorMessage
    } = this.state;

    if (error) {
      throw Error(errorMessage);
    }

    if (loading) {
      return <LoadingScreen />
    }
  
    document.title = data.name;

    // Item Infos
    var itemInfos = [
      { label: "Buy price", value: data.npc_price },
      { label: "Sell price", value: data.npc_price_disposal },
      { label: "Tuning price", value: data.npc_price_tuning },
    ];

    if (this.table == "ship_anchor") {
      itemInfos.unshift(
        { label: "Class", value: data.class_sea },
        { label: "Level", value: data.level_sea },
        { label: "Ship deceleration", value: data.ship_deceleration },
        { label: "Ship turnpower", value: data.ship_turnpower },
      )
    }

    else if (this.table == "ship_body") {
      itemInfos.unshift(
        { label: "Class", value: data.class_sea },
        { label: "Level", value: data.level_sea },
        { label: "Phyiscal defence", value: data.physical_defence },
        { label: "Protection", value: data.protection },
        { label: "DP", value: data.ability_hp },
      )
    }

    else if (this.table == "ship_figure") {
      itemInfos.unshift(
        { label: "Class", value: data.class_sea },
        { label: "Level", value: data.level_sea },
        { label: "Protection", value: data.protection },
        { label: "Balance", value: data.balance },
      )
    }

    else if (this.table == "ship_head_mast") {
      itemInfos.unshift(
        { label: "Class", value: data.class_sea },
        { label: "Level", value: data.level_sea },
        { label: "Ship wind favorable", value: data.ship_wind_favorable },
        { label: "Ship wind adverse", value: data.ship_wind_adverse },
        { label: "Ship turnpower", value: data.ship_turnpower },
      )
    }

    else if (this.table == "ship_main_mast") {
      itemInfos.unshift(
        { label: "Class", value: data.class_sea },
        { label: "Level", value: data.level_sea },
        { label: "Ship wind favorable", value: data.ship_wind_favorable },
        { label: "Ship wind adverse", value: data.ship_wind_adverse },
        { label: "Ship acceleration", value: data.ship_acceleration },
        { label: "Ship deceleration", value: data.ship_deceleration },
        { label: "Ship turnpower", value: data.ship_turnpower },
      )
    }

    else if (this.table == "ship_magic_stone") {
      itemInfos.unshift(
        { label: "Class", value: data.class_sea },
        { label: "Level", value: data.level_sea },
        { label: "EN", value: data.ability_en },
        { label: "EN recovery", value: data.ability_en_recovery },
      )
    }

    else if (this.table == "ship_front") {
      itemInfos.unshift(
        { label: "Class", value: data.class_sea },
        { label: "Level", value: data.level_sea },
        { label: "Physical defence", value: data.physical_defense },
        { label: "Protection", value: data.protection },
        { label: "DP", value: data.ability_hp },
        { label: "Balance", value: data.balance },
      )
    }

    else if (this.table == "ship_normal_weapon") {
      itemInfos.unshift(
        { label: "Class", value: data.class_sea },
        { label: "Level", value: data.level_sea },
        { label: "Damage", value: data.ship_defense },
        { label: "Critical", value: data.critical },
        { label: "Cannon range", value: `${data.ship_range/10}m` },
        { label: "Reloadspeed", value: data.ship_reloadspeed },
        { label: "Guns range", value: `${data.ship_hitrange/10}m` },
      )
    }

    else if (this.table == "ship_special_weapon") {
      itemInfos.unshift(
        { label: "Class", value: data.class_sea },
        { label: "Level", value: data.level_sea },
        { label: "Damage", value: data.ship_defense },
        { label: "Critical", value: data.critical },
        { label: "Range", value: `${data.ship_range/10}m` },
        { label: "Reloadspeed", value: data.ship_reloadspeed },
        { label: "EN usage", value: data.ability_en_usage },
      )
    }

    return (
      <Row>

        <Col md={4}>
          <Infos 
            table={this.table}
            data={data}
            itemInfos={itemInfos}
          />
          <AvailableIn randomBoxes={data.random_boxes} />
        </Col>

        <Col md={8}>
          <DroppedBy table={this.table} droppedBy={data.dropped_by} />
          <ProducedBy recipeData={data.produced_by_recipe} secondJobData={data.produced_by_second_job} />
          <NeededFor recipeData={data.needed_for_recipe} secondJobData={data.needed_for_second_job} />
        </Col>

      </Row>
    )
  }
}