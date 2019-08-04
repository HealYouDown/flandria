import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import AvailableIn from "../detailed_pages_components/AvailableIn";
import DroppedBy from "../detailed_pages_components/DroppedBy";
import Infos from "../detailed_pages_components/Infos";
import Description from "../detailed_pages_components/Description";

export default class PetSkillStone extends React.Component {
  constructor(props) {
    super(props);
    this.table = "pet_skill_stone";
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
      { label: "Level", value: data.level },
      { label: "Cooldown", value: `${data.cooldown/1000}s` },
      { label: "Casttime", value: `${data.casttime/1000}s` },
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
        </Col>

        <Col md={8}>
          <Description desc={data.description} />
          <DroppedBy table={this.table} droppedBy={data.dropped_by} />
        </Col>

      </Row>
    )
  }
}