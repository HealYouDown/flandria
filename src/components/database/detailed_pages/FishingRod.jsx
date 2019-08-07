import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import AvailableIn from "../detailed_pages_components/AvailableIn";
import Infos from "../detailed_pages_components/Infos";
import BonusStats from "../detailed_pages_components/BonusStats";
import LoadingScreen from "../../layout/LoadingScreen";

export default class FishingRod extends React.Component {
  constructor(props) {
    super(props);
    this.table = "fishing_rod";
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
      { label: "Level", value: `${data.level_land}/${data.level_sea}`},
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
          <BonusStats data={data} />
          <AvailableIn randomBoxes={data.random_boxes} />
        </Col>

      </Row>
    )
  }
}