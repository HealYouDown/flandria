import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import DroppedBy from "../detailed_pages_components/DroppedBy";
import Infos from "../detailed_pages_components/Infos";
import LoadingScreen from "../../layout/LoadingScreen";

export default class Bullet extends React.Component {
  constructor(props) {
    super(props);
    this.table = "bullet";
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

    const itemInfos = [
      { label: "Buy price (500/u)", value: `${Math.round(data.npc_price*100, 2)}` },
      { label: "Tradable", value: `${data.tradable ? "True" : "False"}` },
    ]

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