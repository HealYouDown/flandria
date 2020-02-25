import React, { useState } from "react";
import styled from "styled-components";
import Card, { CardHeader, CardBody, CardListBody, ClickableCardListItem } from "../common/Card";
import Icon from "../common/Icon";
import Name from "../common/Name";
import { getBonuses } from "../bonus_codes";
import { getCanEditDrops } from "../auth/auth";
import { Link } from "react-router-dom";

const ClickableItemWrapper = styled.div`
  display: flex;
  flex-flow: row;
  justify-content: center;

  > img {
    flex-grow: 0;
  }

  > div {
    flex-grow: 1;
    display: flex;
    flex-flow: column;
    justify-content: center;

    .sub {
      font-size: 12px;
    }
  }
`

const ClickableItem = ({obj, tablename, link, quantity, probability=null}) => {
  return (
    <ClickableCardListItem link={link}>
      <ClickableItemWrapper>
        <Icon tablename={tablename} icon={obj.icon} />
        <div>
          <Name tablename={tablename} data={obj} />
          {quantity > 1 && (
            <span className="sub">Quantity: {quantity}</span>
          )}
          {probability && (
            <span className="sub">Probability: {probability}%</span>
          )}
        </div>
      </ClickableItemWrapper>
    </ClickableCardListItem>
  )
}


const RightLeftListItemWrapper = styled.li`
  display: flex;
  flex-flow: row;
  justify-content: space-between;
  align-items: center;
`

const RightLeftListItem = (props) => {
  return (
    <RightLeftListItemWrapper>
      {props.children}
    </RightLeftListItemWrapper>
  )
}

/* Infos */

const InfosHeaderWrapper = styled.div`
  display: flex;
  flex-flow: row;
  align-items: center;
`

const Infos = ({tablename, data, itemInfos}) => {
  return (
    <Card>
      <CardHeader>
        <InfosHeaderWrapper>
          <Icon tablename={tablename} icon={data.icon} />
          <Name tablename={tablename} data={data} title />
        </InfosHeaderWrapper>
      </CardHeader>
      <CardListBody>
        <ul>
          {itemInfos.map(i => {
            return (
              <RightLeftListItem>
                <span>{i.label}</span>
                <span>{i.value}</span>
              </RightLeftListItem>
            )
          })}
        </ul>
      </CardListBody>
    </Card>
  )
}

/* Quests */

const Quests = ({quests}) => {
  return (
    <Card>
      <CardHeader>
        <span className="card-title">Quests</span>
      </CardHeader>
      <CardListBody>
        <ul>
          {quests.map(quest => {
            return (
              <ClickableCardListItem link={"/database/quest/" + quest.code}>
                <span className="hover-white">{quest.name}</span>
              </ClickableCardListItem>
            )
          })}
        </ul>
      </CardListBody>
    </Card>
  )
}

/* Drops */

const DropsHeaderWrapper = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;

  > a {
    text-decoration: none;
  }
`

const Drops = ({drops}) => {
  return (
    <Card>
      <CardHeader>
        <DropsHeaderWrapper>
          <span className="card-title">Drops</span>
          {getCanEditDrops() && (
            <Link to={location.pathname + "/edit"}>Edit</Link>
          )}
        </DropsHeaderWrapper>
      </CardHeader>
      {drops.length >= 1 ? (
        <CardListBody>
          <ul>
            {drops.map(drop => {
              return (
                <ClickableItem
                  link={`/database/${drop.item.table}/${drop.item.code}`}
                  obj={drop.item}
                  tablename={drop.item.table}
                  quantity={drop.quantity}
                />
              )
            })}
          </ul>
        </CardListBody>
      ): (
        <CardBody>
          <span>No drops found.</span>
        </CardBody>
      )}
    </Card>
  )
}

/* Bonus Stats */

const BonusStats = ({obj}) => {
  const bonuses = getBonuses(obj);
  if (bonuses.length == 0) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <span className="card-title">Bonus Stats</span>
      </CardHeader>
      <CardListBody>
        <ul>
          {bonuses.map(bonus => {
            return (
              <RightLeftListItem>
                <span>{bonus.name}</span>
                {bonus.operator == "*" ? (
                  <span>{Math.round(bonus.value * 100, 2)}%</span>
                ) : (
                  <span>{bonus.operator} {bonus.value}</span>
                )} 
              </RightLeftListItem>
            )
          })}
        </ul>
      </CardListBody>
    </Card>
  )
}

/* Produced by */

const ProducedBy = ({producedBy}) => {
  const {
    recipe, second_job
  } = producedBy;

  if (recipe.length == 0 && second_job.length == 0) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <span className="card-title">Produced by</span>
      </CardHeader>
      <CardListBody>
        <ul>
          {recipe.map(rec => {
            return (
              <ClickableItem
                link={`/database/recipe/${rec.code}`}
                obj={rec}
                tablename="recipe"
              />
            )
          })}
          {second_job.map(book => {
            return (
              <ClickableItem
                link={`/database/product_book/${book.code}`}
                obj={book}
                tablename="product_book"
              />
            )
          })}
        </ul>
      </CardListBody>
    </Card>
  )
}

/* Needed for */

const NeededFor = ({neededFor}) => {
  const {
    recipe, second_job
  } = neededFor;

  if (recipe.length == 0 && second_job.length == 0) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <span className="card-title">Needed for</span>
      </CardHeader>
      <CardListBody>
        <ul>
          {recipe.map(rec => {
            return (
              <ClickableItem
                link={`/database/recipe/${rec.code}`}
                obj={rec}
                tablename="recipe"
              />
            )
          })}
          {second_job.map(book => {
            return (
              <ClickableItem
                link={`/database/product_book/${book.code}`}
                obj={book}
                tablename="product_book"
              />
            )
          })}
        </ul>
      </CardListBody>
    </Card>
  )
}

/* Available in */

const AvailableIn = ({boxes}) => {
  if (boxes.length == 0) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <span className="card-title">Available in</span>
      </CardHeader>
      <CardListBody>
        <ul>
          {boxes.map(box => {
            return (
              <ClickableItem
                link={`/database/random_box/${box.code}`}
                obj={box}
                tablename="random_box"
              />
            )
          })}
        </ul>
      </CardListBody>
    </Card>
  )
}

/* Upgrade */

const ValueSpan = styled.span`
  transition: color 0.3s;
  color: ${props => props.upgradeLevel >= 1 ? 'lime' : 'inital'};
`;

const UpgradeSliderWrapper = styled.div`
  display: flex;
  flex-flow: row;
  padding: 12px 25px;
  border-bottom: 1px solid black;

  > input {
    flex-grow: 1;
  }
`;

const Upgrade = ({tablename, obj, upgradeData}) => {
  const [upgradeLevel, setUpgradeLevel] = useState(0);
  const weaponTables = ["cariad", "rapier", "dagger", "one_handed_sword", "two_handed_sword", "rifle", "duals"];
  const armorTables = ["coat", "pants", "shoes", "gauntlet"];

  if (upgradeData.length != 16) {
    return null;
  }

  let stats = [];

  if (weaponTables.includes(tablename)) {
    const phMin = obj.physical_attack_min;
    const phMax = obj.physical_attack_max;
    const mgMin = obj.magical_attack_min;
    const mgMax = obj.magical_attack_max;
    const attackSpeed = obj.attack_speed;
    const range = obj.attack_range;

    // All Items have a 'Physical Damage' stat, but just for some it changes when upgrading.
    if (["rapier", "dagger", "one_handed_sword", "two_handed_sword", "rifle", "duals"].includes(tablename)) {
      const newPhMin = Math.floor(phMin + upgradeData[upgradeLevel].value_0);
      const newPhMax = Math.floor(phMax + upgradeData[upgradeLevel].value_0);
      stats.push(
        <RightLeftListItem>
          <span>Phyiscal Damage</span>
          <ValueSpan upgradeLevel={upgradeLevel}>{newPhMin} ~ {newPhMax}</ValueSpan>
        </RightLeftListItem>
      )
    } else {
      stats.push(
        <RightLeftListItem>
          <span>Phyiscal Damage</span>
          <span>{phMin} ~ {phMax}</span>
        </RightLeftListItem>
      )
    }

    // Same goes for 'Magical Damage'.
    if (["cariad", "rapier", "dagger"].includes(tablename)) {
      let minUpValue;
      let maxUpValue;
      if (tablename == "cariad") {
        minUpValue = upgradeData[upgradeLevel].value_1;
        maxUpValue = upgradeData[upgradeLevel].value_1;
      } else {
        minUpValue = upgradeData[upgradeLevel].value_2;
        maxUpValue = upgradeData[upgradeLevel].value_2;
      }
      const newMgMin = Math.floor(mgMin + minUpValue);
      const newMgMax = Math.floor(mgMax + maxUpValue);
      stats.push(
        <RightLeftListItem>
          <span>Magical Damage</span>
          <ValueSpan upgradeLevel={upgradeLevel}>{newMgMin} ~ {newMgMax}</ValueSpan>
        </RightLeftListItem>
      )
    } else {
      stats.push(
        <RightLeftListItem>
          <span>Magical Damage</span>
          <span>{mgMin} ~ {mgMax}</span>
        </RightLeftListItem>
      )
  }

    // Attack Speed
    stats.push(
      <RightLeftListItem>
        <span>Attack Speed</span>
        <span>{attackSpeed/1000}s</span>
      </RightLeftListItem>
    )

    // Range
    stats.push(
      <RightLeftListItem>
        <span>Range</span>
        <span>{range/100}m</span>
      </RightLeftListItem>
    )
  } else if (armorTables.includes(tablename)) {
    const phDef = obj.physical_defense;
    const mgDef = obj.magic_defense;

    // Coat
    if (tablename == "coat") {
      const newPhDef = Math.floor(phDef + upgradeData[upgradeLevel].value_0);
      stats.push(
        <RightLeftListItem>
          <span>Phyiscal Defense</span>
          <ValueSpan upgradeLevel={upgradeLevel}>{newPhDef}</ValueSpan>
        </RightLeftListItem>
      )
    } else {
      stats.push(
        <RightLeftListItem>
          <span>Phyiscal Defense</span>
          <span>{phDef}</span>
        </RightLeftListItem>
      )
    }

    // Pants
    if (tablename == "pants") {
      const newMgDef = Math.floor(mgDef + upgradeData[upgradeLevel].value_0);
      stats.push(
        <RightLeftListItem>
          <span>Magical Defense</span>
          <ValueSpan upgradeLevel={upgradeLevel}>{newMgDef}</ValueSpan>
        </RightLeftListItem>
      )
    } else {
      stats.push(
        <RightLeftListItem>
          <span>Magical Defense</span>
          <span>{mgDef}</span>
        </RightLeftListItem>
      )
    }

    // Gauntlet
    if (tablename == "gauntlet") {
      const hitrate = Math.floor(0 + upgradeData[upgradeLevel].value_0);

      stats.push(
        <RightLeftListItem>
          <span>Hitrate</span>
          <ValueSpan upgradeLevel={upgradeLevel}>{hitrate}</ValueSpan>
        </RightLeftListItem>
      );

      stats.push(
        <RightLeftListItem>
          <span>Attack Speed</span>
          <ValueSpan upgradeLevel={upgradeLevel}>{upgradeLevel}%</ValueSpan>
        </RightLeftListItem>
      );
    }

    // Shoes
    if (tablename == "shoes") {
      const avoidanceRate = Math.floor(0 + upgradeData[upgradeLevel].value_0);

      stats.push(
        <RightLeftListItem>
          <span>Avoidance Rate</span>
          <ValueSpan upgradeLevel={upgradeLevel}>{avoidanceRate}</ValueSpan>
        </RightLeftListItem>
      );

      stats.push(
        <RightLeftListItem>
          <span>Moving Speed</span>
          <ValueSpan upgradeLevel={upgradeLevel}>{upgradeLevel}%</ValueSpan>
        </RightLeftListItem>
      );
    }
  }

  return (
    <Card>
      <CardHeader>
        <span className="card-title">Upgrade</span>
      </CardHeader>
      <CardListBody>
        <UpgradeSliderWrapper>
          <span>{upgradeLevel}</span>
          <input
            type="range"
            onChange={e => setUpgradeLevel(parseInt(e.target.value))}
            min="0"
            max="15"
            value={upgradeLevel}
          />
        </UpgradeSliderWrapper>
        <ul>
          {stats}
        </ul>
      </CardListBody>
    </Card>
  );

}

/* Dropped by */

const DroppedBy = ({droppedBy}) => {
  if (droppedBy.length == 0) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <span className="card-title">Dropped by</span>
      </CardHeader>
      <CardListBody>
        <ul>
          {droppedBy.map(obj => {
            return (
              <ClickableItem
                link={`/database/monster/${obj.monster.code}`}
                obj={obj.monster}
                tablename="monster"
              />
            )
          })}
        </ul>
      </CardListBody>
    </Card>
  )
}

/* TextCard */
const TextCard = ({title, text}) => {
  return (
    <Card>
      <CardHeader>
        <span className="card-title">{title}</span>
      </CardHeader>
      <CardBody>
        <span>{text}</span>
      </CardBody>
    </Card>
  )
}

/* Material stuff */

const ResultItem = ({resultItem}) => {
  return (
    <Card>
      <CardHeader>
        <span className="card-title">Result Item</span>
      </CardHeader>
      <CardListBody>
        <ul>  
          <ClickableItem
            link={`/database/${resultItem.table}/${resultItem.code}`}
            obj={resultItem}
            tablename={resultItem.table}
          />
        </ul>
      </CardListBody>
    </Card>
  )
}

const MaterialList = ({materials}) => {
  return (
    <Card>
      <CardHeader>
        <span className="card-title">Materials</span>
      </CardHeader>
      <CardListBody>
        <ul>
          {materials.map(material => {
            return (
              <ClickableItem
                link={`/database/${material.item.table}/${material.item.code}`}
                obj={material.item}
                tablename={material.item.table}
                quantity={material.quantity}
              />
            )
          })}
        </ul>
      </CardListBody>
    </Card>
  )
}

/* Randombox Content */
const BoxContent = ({content}) => {
  return (
    <Card>
      <CardHeader>
        <span className="card-title">Content</span>
      </CardHeader>
      <CardListBody>
        <ul>
          {content.map(box => {
            return (
              <ClickableItem
                link={`/database/${box.item.table}/${box.item.code}`}
                obj={box.item}
                tablename={box.item.table}
                quantity={box.quantity}
                probability={box.probability}
              />
            )
          })}
        </ul>
      </CardListBody>
    </Card>
  )
}

/* Quest */

const BeforeOrAfterQuest = ({title, quest}) => {
  return (
    <Card>
      <CardHeader><span className="card-title">{title}</span></CardHeader>
      <CardListBody>
        <ul>
          <ClickableCardListItem link={"/database/quest/" + quest.code}>
            <span className="hover-white">{quest.name}</span>
          </ClickableCardListItem>
        </ul>
      </CardListBody>
    </Card>
  )
}

const QuestScrolls = ({scrolls}) => {
  if (scrolls.length == 0) {
    return null;
  }

  return (
    <Card>
      <CardHeader><span className="card-title">Quest Scrolls</span></CardHeader>
      <CardListBody>
        <ul>
          {scrolls.map(scroll => {
            return (
              <ClickableItem
                link={`/database/quest_scroll/${scroll.code}`}
                obj={scroll}
                tablename="quest_scroll"
              />
            )
          })}
        </ul>
      </CardListBody>
    </Card>
  )
}


const NPCWrapper = styled.div`
  display: flex;
  flex-flow: row;
  align-items: center;
  padding: 12px 20px;
`

const QuestMissions = ({missions, description, givenQuestItems}) => {
  return (
    <>
      {missions.map((mission, index) => {
        if ([0, 1, 2, 3, 4, 17].includes(mission.work_type)) {
          return (
            <Card>
              <CardHeader><span className="card-title">{description[`mission_${index+1}`]}</span></CardHeader>
              <CardListBody>
                <ul>
                  {mission.work_type == 0 && (
                    <ClickableItem
                      link={`/database/${mission.item.table}/${mission.item.code}`}
                      obj={mission.item}
                      tablename={mission.item.table}
                      quantity={mission.count}
                    />
                  )}
                  
                  {[1, 4, 17].includes(mission.work_type) && (
                    <>
                      <NPCWrapper>
                        <Icon tablename="npc" icon={mission.npc.icon} />
                        <Name tablename="npc" data={mission.npc} />
                      </NPCWrapper>
                      {givenQuestItems.map(questItemObj => {
                        return (
                          <ClickableItem
                            link={`/database/quest_item/${questItemObj.item.code}`}
                            obj={questItemObj.item}
                            tablename="quest_item"
                            quantity={questItemObj.count}
                          />
                        )
                      })}
                    </>
                  )}

                  {mission.work_type == 3 && (
                    <ClickableItem
                      link={`/database/quest_item/${mission.quest_item.code}`}
                      obj={mission.quest_item}
                      tablename="quest_item"
                      quantity={mission.count}
                    />
                  )}

                  {mission.work_type == 2 && (
                    <ClickableItem
                      link={`/database/monster/${mission.monster.code}`}
                      obj={mission.monster}
                      tablename="monster"
                      quantity={mission.count}
                    />
                  )}
                </ul>
              </CardListBody>
            </Card>
          )
        }
        else {
          // text stuff
          return (
            <Card>
              <CardHeader><span className="card-title">{description[`mission_${index+1}`]}</span></CardHeader>
              <CardBody>
                {mission.work_type == 5 && (
                  <span>{`Equip ${mission.work_value}.`}</span>
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
              </CardBody>
            </Card>
          )
        }
      })}
    </>
  )
}

const Rewards = ({rewards}) => {
  if (rewards.length == 0) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <span className="card-title">Rewards</span>
      </CardHeader>
      <CardListBody>
        <ul>
          {rewards.map(reward => {
            return (
              <ClickableItem
                link={`/database/${reward.item.table}/${reward.item.code}`}
                obj={reward.item}
                tablename={reward.item.table}
                quantity={reward.quantity}
              />
            )
          })}
        </ul>
      </CardListBody>
    </Card>
  )
}

const QuestDescription = ({title, description}) => {
  if (description.length <= 2) {
    return null;
  }

  return (
    <Card>
      <CardHeader>
        <span className="card-title">{title}</span>
      </CardHeader>
      <CardBody>
        {description.split("\\n").map(desc => {
          return (
            <span>{desc} <br/></span>
          )
        })}
      </CardBody>
    </Card>
  )
}

export {
  Infos,
  Quests,
  Drops,
  BonusStats,
  ProducedBy,
  NeededFor,
  AvailableIn,
  Upgrade,
  DroppedBy,
  ResultItem,
  MaterialList,
  TextCard,
  BoxContent,
  BeforeOrAfterQuest,
  QuestScrolls,
  QuestMissions,
  Rewards,
  QuestDescription,
}
