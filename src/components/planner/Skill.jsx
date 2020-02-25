import React from "react";
import styled from "styled-components";
import breakpoint from "../breakpoint";
import { BLUE } from "../colors";
import SkillDescription from "./SkillDescription";

const SkillWrapper = styled.div`
  position: absolute;
  display: flex;
  flex-flow: row;
  align-items: center;

  ${props => `top: ${props.pos[0]}px; left: ${props.pos[1]}px;`};
`

const SkillIconWrapper = styled.div`
  position: relative;
  height: 32px;
`

const SkillLevel = styled.span`
  position: absolute;
  bottom: 0;
  left: 0;
  background: rgba(0, 0, 0, 0.7);
  color: #fff;
  font-size: 14px;
`

const SkillIconEffectWrapper = styled.div`
  ${props => {
    if (!props.allowed && !props.skilled) {
      return `
        -webkit-filter: grayscale(100%);
        -moz-filter: grayscale(100%);
        -o-filter: grayscale(100%);
        -ms-filter: grayscale(100%);
        filter: grayscale(100%); 
      `;
    } else if (props.allowed && !props.skilled) {
      return `
        filter: brightness(50%);
        -webkit-filter: brightness(50%);
        -moz-filter: brightness(50%);  
      `;
    }
  }}
`

const LevelButton = styled.button`
  border: none;
  width: 10px;
  font-size: 14px;
  overflow: hidden;
  height: 32px;
  padding: 0px;
  color: white;
  background-color: ${BLUE};

  visibility: visible;
  ${breakpoint("md")`
    visibility: hidden;
  `};

  ${props => props.right ? "border-top-right-radius: 5px; border-bottom-right-radius: 5px;"
                         : "border-top-left-radius: 5px; border-bottom-left-radius: 5px;"};
`

const getCurrentCode = (baseSkillCode, skillLevel) => {
  let baseCode = baseSkillCode.substring(0, baseSkillCode.length - 2);
  if (skillLevel <= 9) {
    return `${baseCode}0${skillLevel}`
  }
  else {
    return `${baseCode}${skillLevel}`
  }
}

const getNextCode = (baseSkillCode, skillLevel) => {
  let baseCode = baseSkillCode.substring(0, baseSkillCode.length - 2);
  let nextLevel = skillLevel + 1;
  if (nextLevel <= 9) {
    return `${baseCode}0${nextLevel}`
  }
  else {
    return `${baseCode}${nextLevel}`
  }
}

const Skill = ({baseSkillCode, plannerClass, pos, skills, skillData, currentLevel, levelDown, levelUp}) => {
  const skill = skills[baseSkillCode];

  const skillLevel = skill.level;
  const isSkilled = skill.level > 0;
  const isAllowed = skill.allowed;

  const currentSkillCode = getCurrentCode(baseSkillCode, skillLevel);
  const currentData = skillData[currentSkillCode];

  const nextSkillCode = getNextCode(baseSkillCode, skillLevel);
  const nextData = skillData[nextSkillCode] || {};

  const levelUpSkill = (event) => {
    levelUp(baseSkillCode, event.shiftKey);
  }

  const levelDownSkill = (event) => {
    event.preventDefault();
    levelDown(baseSkillCode, event.shiftKey);
  }

  return (
    <>
      <SkillDescription
        baseSkillCode={baseSkillCode}
        currentData={currentData}
        nextData={nextData}
        currentLevel={currentLevel}
      />

      <SkillWrapper pos={pos} data-tip data-for={baseSkillCode}>
        <LevelButton left onClick={levelDownSkill}>-</LevelButton>
        <SkillIconWrapper>
          <SkillIconEffectWrapper allowed={isAllowed} skilled={isSkilled}>
            <img
              onClick={levelUpSkill}
              onContextMenu={levelDownSkill}
              src={`/static/assets/skill_icons/${plannerClass}/${currentData.icon}`}
            />
          </SkillIconEffectWrapper>
          <SkillLevel>{skillLevel}</SkillLevel>
        </SkillIconWrapper>
        <LevelButton right onClick={levelUpSkill}>+</LevelButton>
      </SkillWrapper>
    </>
  )
}

export default Skill;
export {
  getNextCode,
}