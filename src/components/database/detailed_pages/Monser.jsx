import { FaEdit } from "react-icons/fa";
import { Row, Col } from "react-grid-system";
import React from "react";

import { fetchDetailedPageData } from "../../api";
import AuthService from "../../AuthService";
import CardList, { ClickableListItem } from "../../shared/CardList";
import EditMonsterModal from "./MonsterEdit";
import Icon from "../Icon";
import Infos from "../detailed_pages_components/Infos";
import Name from "../Name";
import LoadingScreen from "../../layout/LoadingScreen";

import "../../../styles/fa-icon.css";

export default class Monster extends React.Component {
  constructor(props) {
    super(props);
    this.table = "monster";
    this.code = this.props.match.params.code;
    this.auth = new AuthService();

    this.state = {
      loading: true,
      data: {},
      error: false,
      errorMessage: "",
      modalOpen: false,
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
      errorMessage,
      modalOpen,
    } = this.state;

    if (error) {
      throw Error(errorMessage);
    }

    if (loading) {
      return <LoadingScreen />
    }

    document.title = data.name;

    const itemInfos = [
      { label: "Level", value: data.level },
      { label: "Health points", value: data.hp },
      { label: "Experience", value: data.experience },
      { label: "Range", value: data.range },
      { label: "Damage", value: `${data.min_dmg} ~ ${data.max_dmg}` },
      { label: "Physical defense", value: data.physical_defense },
      { label: "Magical defense", value: data.magical_defense },
    ]

    // Drops take up 8 cols if there are no quests.
    const dropsColWidth = this.state.data.quests.length >= 1 ? 4 : 8;

    const dropsHeader = (
      <div style={{display: "flex", justifyContent: "space-between"}}>
        <span className="card-title">Drops</span>
        {this.auth.canEditDrops() && (
          <FaEdit
            onClick={() => this.setState({modalOpen: true})}
            className="fa-icon" 
          />
        )}
      </div>
    )

    return (
      <>
        <EditMonsterModal 
          data={data} 
          modalOpen={modalOpen}
          changeState={this.setState.bind(this)}
        />

        <Row>

          <Col md={4}>
            <Infos 
              table={this.table}
              data={data}
              itemInfos={itemInfos}
            />
          </Col>

          {data.quests.length >= 1 && (
            <Col md={4}>
              <CardList header={true} list={true}>
                <span className="card-title">Quests</span>
                {data.quests.map((quest, i) => {
                  return (
                    <ClickableListItem key={i} link={`/database/quest/${quest.code}`}>
                      <span>{quest.name}</span>
                    </ClickableListItem>
                  )
                })}
              </CardList>
            </Col>
          )}

          <Col md={dropsColWidth}>
            {data.drops.length == 0
              ? (
                <CardList header={true} padding={20}>
                  {dropsHeader}
                  <span>No drops were found.</span>
                </CardList>
              )
              : (
                <CardList header={true} list={true}>
                  {dropsHeader}
                  {data.drops.map((drop, i) => {
                    return (
                      <ClickableListItem key={i} hover={false} link={`/database/${drop.item.table}/${drop.item.code}`}>
                        <Icon table={drop.item.table} data={drop.item} />
                        <div style={{lineHeight: "1"}}>
                          <Name table={drop.item.table} data={drop.item} />
                          {drop.quantity != 1 && (
                            <>
                              <br />
                              <span className="subs">Quantity: {drop.quantity}</span>
                            </>
                          )}
                        </div>
                      </ClickableListItem>
                    )
                  })}
                </CardList>
              )
            }
          </Col>

        </Row>
      </>
    )
  }
}