import React from "react";
import { Row, Col } from "react-grid-system";
import { fetchDetailedPageData } from "../../api";
import Infos from "../detailed_pages_components/Infos";
import CardList, { ClickableListItem } from "../../shared/CardList";
import Icon from "../Icon";
import Name from "../Name";


const QuestDescription = ({title, description}) => {
  if (description.length <= 2) {
    return null;
  }

  return (
    <CardList header={true} padding={20}>
      <span className="card-title">{title}</span>
      <>
        {description.split("\\n").map((desc, i) => {
          return (
            <span key={i}>
              {desc}
              <br />
            </span>
          )
        })}
      </>
    </CardList>
  )
}


export default class Quest extends React.Component {
  constructor(props) {
    super(props);
    this.table = "quest";
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

  componentWillReceiveProps(nextProps) {
    if (nextProps.match.params.code != this.code) {
      this.code = nextProps.match.params.code
      fetchDetailedPageData(this.table, this.code, this.setState.bind(this));
    }
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

    const desc = data.descriptions.filter(d => d.language_code == "en")[0];
    const descColWidth = (data.missions.length >= 1 || data.selectable_items.length >= 1) ? 4 : 8;
    const itemInfos = [
      { label: "Class", value: data.player_class },
      { label: "Level", value: data.level },
      { label: "Location", value: data.location },
      { label: "EXP reward", value: data.exp_reward },
      { label: "Gelt reward", value: data.money_reward },
      { label: "Start map", value: data.source_area.name },
      { label: "Start NPC", value: data.source_object.name },
      { label: "Finish NPC", value: data.supplier.name }  
    ]

    return (
      <Row>

        <Col md={4}>
          <Infos 
            table={this.table}
            data={data}
            itemInfos={itemInfos}
          />

          {data.before_quest_code && (
            <CardList header={true} list={true}>
              <span className="card-title">Before quest</span>
              <ClickableListItem link={`/database/quest/${data.before_quest_code}`}>
                <span>{data.before_quest.name}</span>
              </ClickableListItem>
            </CardList>
          )}

          {data.after_quests.length >= 1 && (
            <CardList header={true} list={true}>
              <span className="card-title">After quest</span>
              <ClickableListItem link={`/database/quest/${data.after_quests[0].code}`}>
                <span>{data.after_quests[0].name}</span>
              </ClickableListItem>
            </CardList>
          )}

          {data.quest_scrolls.length >= 1 && (
            <CardList header={true} list={true}>
              <span className="card-title">Quest scroll</span>
              <ClickableListItem link={`/database/quest_scroll/${data.quest_scrolls[0].code}`}>
                <Icon table="quest_scroll" data={data.quest_scrolls[0]} />
                <Name table="quest_scroll" data={data.quest_scrolls[0]} />
              </ClickableListItem>
            </CardList>
          )}
        </Col>

        {(data.missions.length >= 1 || data.selectable_items.length >= 1) && (
          <Col md={4}>

            {data.missions.map((mission, i) => {

              if ([0, 1, 4, 17, 3, 2].includes(mission.work_type)) {
                return (
                  <CardList key={i} header={true} list={true}>
                    <span className="card-title">{desc[`mission_${i + 1}`]}</span>
  
                      {mission.work_type == 0 && (
                        <ClickableListItem hover={false} link={`/database/${mission.item.table}/${mission.item.code}`}>
                          <Icon table={mission.item.table} data={mission.item} />
                          <div style={{lineHeight: "1.0"}}>
                            <Name table={mission.item.table} data={mission.item} />
                            <br />
                            <span className="subs">Quantity: {mission.count}</span>
                          </div>
                        </ClickableListItem>
                      )}
  
                      {[1, 4, 17].includes(mission.work_type) && (
                        <>
                          <ClickableListItem link="#">
                            <Icon npc={true} data={mission.npc} />
                            <Name table={null} data={mission.npc} />
                          </ClickableListItem>
                          {data.give_descriptions.map((d, i) => {
                            return (
                              <ClickableListItem key={i} hover={false} link={`/database/quest_item/${d.item.code}`}>
                                <Icon table="quest_item" data={d.item} />
                                <Name table="quest_item" data={d.item} />
                              </ClickableListItem>
                            )
                          })}
                        </>
                      )}
  
                      {mission.work_type == 3 && (
                        <ClickableListItem hover={false} link={"/database/quest_item/" + mission.quest_item_code}>
                          <Icon table="quest_item" data={mission.quest_item} />
                          <div style={{lineHeight: "1.0"}}>
                            <Name table="quest_item" data={mission.quest_item} />
                            <br />
                            <span className="subs">Quantity: {mission.count}</span>
                          </div>
                        </ClickableListItem>
                      )}
  
                    {mission.work_type == 2 && (
                      <ClickableListItem hover={false} link={"/database/monster/" + mission.monster_code}>
                        <Icon table="monster" data={mission.monster} />
                        <div style={{lineHeight: "1.0"}}>
                          <Name table="monster" data={mission.monster} />
                          <br />
                          <span className="subs">Amount: {mission.count}</span>
                        </div>
                      </ClickableListItem>
                    )}
  
                  </CardList>
                )
              }
              else {
                return (
                  <CardList key={i} header={true} list={false} padding={20}>
                    <span className="card-title">{desc[`mission_${i + 1}`]}</span>

                    {mission.work_type == 5 && (
                      <span>{`Equip ${mission.work_value}`}</span>
                    )}

                    {mission.work_type == 9 && (
                      (mission.work_value == "0")
                        ? <span>Use Land Skill book.</span>
                        : <span>Use Sea Skill book.</span>
                    )}

                    {mission.work_type == 10 && (
                      (mission.work_value == "0")
                        ? <span>Use a Land Skill point.</span>
                        : <span>Use a Sea Skill point.</span>
                    )}

                    {mission.work_type == 11 && (
                      <span>Add a potion to your quick slot bar.</span>
                    )}

                    {mission.work_type == 12 && (
                      <span>Add a skill to your quick slot bar.</span>
                    )}

                    {mission.work_type == 13 && (
                      <span>Build a ship.</span>
                    )}

                    {mission.work_type == 14 && (
                      <span>Tune your ship.</span>
                    )}

                    {mission.work_type == 15 && (
                      <span>Equip shells for the ship.</span>
                    )}

                    {mission.work_type == 16 && (
                      <span>Change weapons.</span>
                    )}
                  </CardList>
                )
              }
            })}

            {data.selectable_items.length >= 1 && (
              <CardList header={true} list={true}>
                <span className="card-title">Rewards</span>
                {data.selectable_items.map((reward, i) => {
                  return (
                    <ClickableListItem key={i} hover={false} link={`/database/${reward.item.table}/${reward.item}`}>
                      <Icon table={reward.item.table} data={reward.item} />
                      <div>
                        <Name table={reward.item.table} data={reward.item} />
                        <br />
                        <span className="subs">Quantity: {reward.amount}</span>
                      </div>
                    </ClickableListItem>
                  )
                })}
              </CardList>
            )}
          </Col>
        )}

        <Col md={descColWidth}>
          <QuestDescription title="Description" description={desc.desc} />
          <QuestDescription title="Pre Dialog" description={desc.pre_dialog} />
          <QuestDescription title="Start Dialog" description={desc.start_dialog} />
          <QuestDescription title="Run Dialog" description={desc.run_dialog} />
          <QuestDescription title="Finish Dialog" description={desc.finish_dialog} />
        </Col>

      </Row>
    )
  }
}