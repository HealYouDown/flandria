import React from "react";
import ReactTooltip from "react-tooltip";
import styled from "styled-components";
import "../../styles/skill-description.css";

const SkillDescriptionHeader = styled.div`
  display: flex;
  flex-flow: row;
  justify-content: space-between;
`;

const SkillName = styled.span`
  color: lime;
  font-size: 16px;
`;

const SkillLevel = styled.span`
  margin-left: 5px;
  background-color: #5695d4;
  border-radius: 7px;
  padding-left: 5px;
  padding-right: 5px;
  color: #fff;
`;

const SkillDescriptionSubHeader = styled.div``;

const SkillDescriptionDivider = styled.hr`
  border-top: 1px solid black;
`;

const StatsWrapper = styled.div`
  > div {
    display: flex;
    justify-content: space-between;
  }
`;

const StatsRequiredLevel = styled.span`
  ${props => !props.allowed ? "color: red" : ""};
`

const SkillDescriptionText = styled.div`
  margin-top: 3px;
  text-align: center;
`

const NextLevel = styled.span`
  display: block;
  color: #fff;
  text-align: center;
`

const Stats = ({currentLevel, data}) => {
  const isAllowed = currentLevel >= data.required_level;

  return (
    <>
      <StatsWrapper>
        <div>
          <span>Req. Level</span>
          <StatsRequiredLevel allowed={isAllowed}>{data.required_level}</StatsRequiredLevel>
        </div>
        <div>
          <span>Mp</span>
          <span>{data.mana_consumption}</span>
        </div>
        <div>
          <span>Cooldown</span>
          <span>{data.cooldown/1000}s</span>
        </div>
      </StatsWrapper>
      <SkillDescriptionText>
        {data.description.split("\\n").map(desc => {
          return (
            <span>
              {desc}
              <br />
            </span>
          )
        })}
      </SkillDescriptionText>
    </>
  )
}

const SkillDescription = ({baseSkillCode, currentData, nextData, currentLevel}) => {
  const name = currentData.name;
  const skillLevel = currentData.skill_level;
  const maxLevel = currentData.max_level;
  const nextLevel = nextData.skill_level || -1;

  return (
    <ReactTooltip
      id={baseSkillCode}
      effect="solid"
      place="right"
      clickable={true}
      multiline={true}
      delayHide={50}
      delayShow={150}
      className="skill-description"
    >
      <SkillDescriptionHeader>
        <SkillName>{name}</SkillName>
        <SkillLevel>{skillLevel}/{maxLevel}</SkillLevel>
      </SkillDescriptionHeader>

      <SkillDescriptionSubHeader>
        <span>{currentData.class_land}</span>
      </SkillDescriptionSubHeader>

      <SkillDescriptionDivider />

      {skillLevel >= 1 && (
        <>
          <Stats
            currentLevel={currentLevel}
            data={currentData}
          />
          {skillLevel != maxLevel && (
            <SkillDescriptionDivider />
          )}
        </>
      )}

      {skillLevel != maxLevel && (
        <>
          <NextLevel>Next Level: ({nextLevel})</NextLevel>
          <Stats
            currentLevel={currentLevel}
            data={nextData}
          />
        </>
      )}

    </ReactTooltip>
  )
}

export default SkillDescription;