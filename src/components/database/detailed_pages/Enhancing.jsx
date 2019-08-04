import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import AvailableIn from "../detailed_pages_components/AvailableIn";
import Infos from "../detailed_pages_components/Infos";
import Description from "../detailed_pages_components/Description";
import DroppedBy from "../detailed_pages_components/DroppedBy";

export default class Enhancing extends React.Component {
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
          <DroppedBy droppedBy={data.dropped_by} />
        </Col>

      </Row>
    )
  }
}