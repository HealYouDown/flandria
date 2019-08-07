import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import AvailableIn from "../detailed_pages_components/AvailableIn";
import BonusStats from "../detailed_pages_components/BonusStats";
import DroppedBy from "../detailed_pages_components/DroppedBy";
import Infos from "../detailed_pages_components/Infos";
import NeededFor from "../detailed_pages_components/NeededFor";
import ProducedBy from "../detailed_pages_components/ProducedBy";
import LoadingScreen from "../../layout/LoadingScreen";

export default class Accessory extends React.Component {
  constructor(props) {
    super(props);
    this.table = "accessory";
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
      { label: "Class", value: data.class_land },
      { label: "Gender", value: data.gender },
      { label: "Level", value: `${data.level_land}/${data.level_sea}` },
      { label: "Sell price", value: data.npc_price_disposal },
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
          <AvailableIn randomBoxes={data.random_boxes} />
          <ProducedBy recipeData={data.produced_by_recipe} secondJobData={data.produced_by_second_job} />
          <NeededFor recipeData={data.needed_for_recipe} secondJobData={data.needed_for_second_job} />
        </Col>

        <Col md={8}>
          <BonusStats data={data} />
          <DroppedBy table={this.table} droppedBy={data.dropped_by} />
        </Col>

      </Row>
    )
  }
}