import React from "react";
import styled from "styled-components";
import { Link } from "react-router-dom";
import RightArrow from "../common/RightArrow";


const CardWrapper = styled.div`
  display: flex;
  flex-flow: column;
  margin-top: 15px;
`;

const CardBody = styled.div`
  background: rgba(0, 0, 0, 0.5);
  padding: 12px 20px;
`;

const CardHeader = styled.div`
  background: rgba(0, 0, 0, 0.7);
  border-top-right-radius: 5px;
  border-top-left-radius: 5px;
  padding: 12px 20px;

  span.card-title {
    font-size: 20px;
  }
`;

const CardListBodyWrapper = styled.div`
  background: rgba(0, 0, 0, 0.5);

  > ul {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  li {
    padding: 12px 20px;
  }

  li:not(:first-child) {
    border-top: 1px solid black;
  }
`

const ClickableCardListItemWrapper = styled.li`
  cursor: pointer;

  > a {
    text-decoration: none;
    display: flex;
    flex-flow: row;
    margin: -12px -20px;
    padding: 12px 20px;

    > div {
      flex-grow: 1;
    }
    > .right-arrow {
      flex-grow: 0;
    }
  }

  &:hover {
    background: rgba(0, 0, 0, 0.7);

    .right-arrow path {
      fill: white;
    }

    *.hover-white {
      color: white;
    }
  }
`

const Card = (props) => {
  return (
    <CardWrapper>
      {props.children}
    </CardWrapper>
  )
}

const CardListBody = (props) => {
  return (
    <CardListBodyWrapper>
      {props.children}
    </CardListBodyWrapper>
  )
}

const ClickableCardListItem = (props) => {
  return (
    <ClickableCardListItemWrapper>
      <Link to={props.link}>
        <div>
          {props.children}
        </div>
        <RightArrow />
      </Link>
    </ClickableCardListItemWrapper>
  )
}

export default Card;
export {
  CardHeader,
  CardBody,
  CardListBody,
  ClickableCardListItem,
}