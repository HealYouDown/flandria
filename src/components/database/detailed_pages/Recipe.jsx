import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import AvailableIn from "../detailed_pages_components/AvailableIn";
import CardList, { ClickableListItem } from "../../shared/CardList";
import DroppedBy from "../detailed_pages_components/DroppedBy";
import Icon from "../Icon";
import Infos from "../detailed_pages_components/Infos";
import Name from "../Name";

export default class Recipe extends React.Component {
  constructor(props) {
    super(props);
    this.table = "recipe";
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
          <DroppedBy table={this.table} droppedBy={data.dropped_by} />
          <AvailableIn randomBoxes={data.random_boxes} />

        </Col>

        <Col md={8}>

          <CardList header={true} list={true}>
            <span className="card-title">Result Item</span>
            <ClickableListItem hover={false} link={`/database/${data.result_item.table}/${data.result_item.code}`}>
              <Icon table={data.result_item.table} data={data.result_item} />
              <div style={{lineHeight: "1"}}>
                <Name table={data.result_item.table} data={data.result_item} />
                <br />
                <span className="subs">Quantity: {data.result_quantity}</span>
              </div>
            </ClickableListItem>
          </CardList>

          <CardList header={true} list={true}>
            <span className="card-title">Materials</span>
            {[1, 2, 3, 4, 5, 6].map(n => {
              var materialCode = data[`material_${n}_code`];
              if (materialCode == "#") {
                return null;
              }
              var materialQuantity = data[`material_${n}_quantity`];
              var material = data[`material_${n}`];
              return (
                <ClickableListItem key={n} hover={false} link={`/database/${material.table}/${material.code}`}>
                  <Icon table={material.table} data={material} />
                  <div style={{lineHeight: "1"}}>
                    <Name table={material.table} data={material} />
                    <br />
                    <span className="subs">Quantity: {materialQuantity}</span>
                  </div>
                </ClickableListItem>
              )
            })}
          </CardList>

        </Col>

      </Row>
    )
  }
}