import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import AvailableIn from "../detailed_pages_components/AvailableIn";
import BonusStats from "../detailed_pages_components/BonusStats";
import DroppedBy from "../detailed_pages_components/DroppedBy";
import Infos from "../detailed_pages_components/Infos";

export default class DressAndHat extends React.Component {
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

    const itemInfos = [
      { label: "Class", value: data.class_land },
      { label: "Gender", value: data.gender },
      { label: "Level", value: `${data.level_land}/${data.level_sea}` },
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
          <DroppedBy table={this.table} droppedBy={data.dropped_by} />
        </Col>

        <Col md={8}>
          <BonusStats data={data} />
          <AvailableIn randomBoxes={data.random_boxes} />
        </Col>

      </Row>
    )
  }
}