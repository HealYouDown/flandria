import React from "react";
import { Row, Col } from "react-grid-system";
import Card, { CardHeader, CardListBody, ClickableCardListItem } from "../../common/Card";
import styled from "styled-components";
import Icon from "../../common/Icon";
import Name from "../../common/Name";
import { DroppedBy, SoldBy } from "../DetailedViewComponents";
import Ad from "../../common/Ad";

const InfosHeaderWrapper = styled.div`
  display: flex;
  flex-flow: row;
  align-items: center;
`

const QuestScroll = ({tablename, data}) => {
  const {
    obj, dropped_by, quests_by_scroll, sold_by,
  } = data;

  return (
    <>
      <Row>
        <Col md={4}>
          <Card>
            <CardHeader>
              <InfosHeaderWrapper>
                <Icon tablename={tablename} icon={obj.icon} />
                <Name tablename={tablename} data={obj} title />
              </InfosHeaderWrapper>
            </CardHeader>
            <CardListBody>
              <ul>
                {quests_by_scroll.map(quest => {
                  return (
                    <ClickableCardListItem
                      link={"/database/quest/" + quest.code}
                    >
                      <span className="hover-white">{quest.name}</span>
                    </ClickableCardListItem>
                  )
                })}
              </ul>
            </CardListBody>
          </Card>
        </Col>
      
        <Col md={8}>
          <DroppedBy droppedBy={dropped_by} />
          <SoldBy soldBy={sold_by} />
        </Col>
      </Row>
      <Ad slot="1071258842" />
    </>
  )
}

export default QuestScroll;