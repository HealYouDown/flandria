import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import DroppedBy from "../detailed_pages_components/DroppedBy";
import Infos from "../detailed_pages_components/Infos";

export default class FlagAndShell extends React.Component {
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
      return null;
    }
  
    document.title = data.name;

    var itemInfos = [];
    if (this.table == "shell") {
      itemInfos = [
        { label: "Level", value: data.level_sea },
        { label: "Damage", value: data.damage },
      ]
    }
    else if (this.table == "ship_flag") {
      itemInfos = [
        { label: "Level", value: data.level_sea },
        { label: "Buy price", value: data.npc_price },
        { label: "Sell price", value: data.npc_price_disposal },
        { label: "Tuning price", value: data.npc_price_tuning },
      ]
    }

    return (
      <Row>

        <Col md={4}>
          <Infos 
            table={this.table}
            data={data}
            itemInfos={itemInfos}
          />
        </Col>

        <Col md={8}>
          <DroppedBy table={this.table} droppedBy={data.dropped_by} />
        </Col>

      </Row>
    )
  }
}