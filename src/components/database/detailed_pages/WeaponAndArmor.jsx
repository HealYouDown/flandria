import React from "react";
import { Row, Col } from "react-grid-system";
import { fetchDetailedPageData } from "../../api";
import Infos from "../detailed_pages_components/Infos";
import BonusStats from "../detailed_pages_components/BonusStats";
import AvailableIn from "../detailed_pages_components/AvailableIn";
import DroppedBy from "../detailed_pages_components/DroppedBy";
import ProducedBy from "../detailed_pages_components/ProducedBy";
import NeededFor from "../detailed_pages_components/NeededFor";
import Upgrade from "../detailed_pages_components/Upgrade";

export default class WeaponAndArmor extends React.Component {
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
          <BonusStats data={data} />
          <ProducedBy recipeData={data.produced_by_recipe} secondJobData={data.produced_by_second_job} />
          <NeededFor recipeData={data.needed_for_recipe} secondJobData={data.needed_for_second_job} />
          <AvailableIn randomBoxes={data.random_boxes} />
        </Col>

        <Col md={8}>
          {this.table != "shield" && (
            <Upgrade table={this.table} data={data} />
          )}
          <DroppedBy droppedBy={data.dropped_by} />
        </Col>

      </Row>
    )
  }
}