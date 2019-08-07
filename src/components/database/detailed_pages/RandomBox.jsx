import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import AvailableIn from "../detailed_pages_components/AvailableIn";
import DroppedBy from "../detailed_pages_components/DroppedBy";
import Infos from "../detailed_pages_components/Infos";
import NeededFor from "../detailed_pages_components/NeededFor";
import ProducedBy from "../detailed_pages_components/ProducedBy";
import CardList, { ClickableListItem } from "../../shared/CardList";
import Icon from "../Icon";
import Name from "../Name";
import LoadingScreen from "../../layout/LoadingScreen";

export default class RandomBox extends React.Component {
  constructor(props) {
    super(props);
    this.table = "random_box";
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
          <DroppedBy table={this.table} droppedBy={data.dropped_by} />
          <ProducedBy recipeData={data.produced_by_recipe} secondJobData={data.produced_by_second_job} />
          <NeededFor recipeData={data.needed_for_recipe} secondJobData={data.needed_for_second_job} />
        </Col>

        <Col md={8}>
          <CardList header={true} list={true}>
            <span className="card-title">Content</span>
            {Array.from(Array(61).keys()).map(n => {
              let itemCode = data[`item_${n}_code`]
              if (itemCode == "#") {
                return null;
              }
              let itemQuantity = data[`item_${n}_quantity`]
              let item, link;
              if (itemCode == "money") {
                item = { "name": "Gelt", "icon": "def004.png", "table": null };
                link = "#";
              }
              else {
                item = this.state.data[`item_${n}`];
                link = `/database/${item.table}/${item.code}`;
              }
              
              return (
                <ClickableListItem key={n} hover={false} link={link}>
                  <Icon table={item.table} data={item} />
                  <div style={{lineHeight: "1"}}>
                    <Name table={item.table} data={item} />
                    <br />
                    <span className="subs">Quantity: {itemQuantity}</span>
                  </div>
                </ClickableListItem>
              )
            })
            }
          </CardList>
        </Col>

      </Row>
    )
  }
}