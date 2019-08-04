import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import Infos from "../detailed_pages_components/Infos";
import ProducedBy from "../detailed_pages_components/ProducedBy";
import NeededFor from "../detailed_pages_components/NeededFor";

export default class FishingItem extends React.Component {
  constructor(props) {
    super(props);
    this.table = "fishing_material";
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
        </Col>

        <Col md={8}>
          <ProducedBy recipeData={data.produced_by_recipe} secondJobData={data.produced_by_second_job} />
          <NeededFor recipeData={data.needed_for_recipe} secondJobData={data.needed_for_second_job} />
        </Col>

      </Row>
    )
  }
}