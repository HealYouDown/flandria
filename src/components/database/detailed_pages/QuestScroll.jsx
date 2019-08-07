import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import CardList, { ClickableListItem } from "../../shared/CardList";
import Icon from "../Icon";
import Name from "../Name";
import LoadingScreen from "../../layout/LoadingScreen";

import "../detailed_pages_components/Infos.css";

export default class QuestScroll extends React.Component {
  constructor(props) {
    super(props);
    this.table = "quest_scroll";
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

    return (
      <Row>
        <Col md={4}>
          <CardList header={true} list={true}>
            <div className="info-header">
              <Icon table={this.table} data={data} />
              <Name table={this.table} data={data} />
            </div>
            <ClickableListItem hover={false} link={`/database/quest/${data.quest_code}`}>
              <Name table="quest" data={data.quest} />
            </ClickableListItem>
          </CardList>
        </Col>
      </Row>
    )
  }
}