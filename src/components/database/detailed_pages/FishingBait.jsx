import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import Infos from "../detailed_pages_components/Infos";

export default class FishingBait extends React.Component {
  constructor(props) {
    super(props);
    this.table = "fishing_bait";
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
      { label: "Buy price", value: data.npc_price },
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

      </Row>
    )
  }
}