import React from "react";
import styled from "styled-components";
import { TileBase } from "../common/StyleMixins";
import Icon from "../common/Icon";

const Wrapper = styled.div`
  padding-top: 15px;
  padding-bottom: 15px;
  padding-left: 10px;
  padding-right: 10px;
  border-radius: 7px;
  display: flex;
  cursor: pointer;

  ${props => props.active ? `
  background: rgba(0, 0, 0, 0.5);
  ` : `
  background: rgba(0, 0, 0, 0.2);
  `};
`;

const MonsterName = styled.span`
  color: ${props => props.active ? props.color : "gray"};
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
`

const InfoWrapper = styled.div`
  display: flex;
  flex-flow: column;
  justify-content: center;
`

const IconWrapper = styled.div`
  ${props => props.active ? `` : `
  filter: brightness(50%);
  -webkit-filter: brightness(50%);
  -moz-filter: brightness(50%);  
  `};

`

const MonsterShowCheckbox = ({monster, onChange, color, active}) => {
  return (
    <Wrapper active={active} onClick={onChange}>
      <IconWrapper active={active}>
        <Icon tablename="monster" icon={monster.icon} />
      </IconWrapper>
      <InfoWrapper>
        <MonsterName color={color} active={active}>
          {monster.name}
        </MonsterName>
      </InfoWrapper>
    </Wrapper>
  )
}

export default MonsterShowCheckbox