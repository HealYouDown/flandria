import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import AvailableIn from "../detailed_pages_components/AvailableIn";
import DroppedBy from "../detailed_pages_components/DroppedBy";
import Infos from "../detailed_pages_components/Infos";
import NeededFor from "../detailed_pages_components/NeededFor";
import ProducedBy from "../detailed_pages_components/ProducedBy";
import Description from "../detailed_pages_components/Description";

export default class Consumable extends React.Component {
  constructor(props) {
    super(props);
    this.table = "consumable";
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
      { label: "Cooldown", value: `${data.cooltime/1000}s` },
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
          <ProducedBy recipeData={data.produced_by_recipe} secondJobData={data.produced_by_second_job} />
          <NeededFor recipeData={data.needed_for_recipe} secondJobData={data.needed_for_second_job} />
          <AvailableIn randomBoxes={data.random_boxes} />
        </Col>

        <Col md={8}>
          <Description desc={data.description} />
          <DroppedBy table={this.table} droppedBy={data.dropped_by} />
        </Col>

      </Row>
    )
  }
}