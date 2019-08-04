import React from "react";
import "./Skill.css";
import { isMobile } from "react-device-detect";
import { FaMinus, FaPlus } from "react-icons/fa";
import SkillDescription from "./SkillDescription";

function getCurrentCode(code, level) {
  let baseCode = code.substring(0, code.length - 2);
  if (level <= 9) {
    return `${baseCode}0${level}`
  }
  else {
    return `${baseCode}${level}`
  } 
}


function getNextCode(code, level) {
  let baseCode = code.substring(0, code.length - 2);
  let nextLevel = level + 1;
  if (nextLevel <= 9) {
    return `${baseCode}0${nextLevel}`
  }
  else {
    return `${baseCode}${nextLevel}`
  }  
}


const Skill = ({code, plannerClass, pos, skills, data, selectedLevel, levelUpFunction, levelDownFunction}) => {
  const posStyle = {position: "absolute", top: `${pos[0]}px`, left: `${pos[1]}px`}
  const levelMinusClassName = isMobile ? "level-button level-button-minus" : "level-button level-button-minus hidden";
  const levelPlusClassName = isMobile ? "level-button level-button-plus" : "level-button level-button-plus hidden";
  const currentLevel = skills[code].level;
  const allowed = skills[code].allowed;
  const effectClassName = `skill-icon-effect-wrapper ${allowed ? "allowed" : ""} ${currentLevel >= 1 ? "skilled" : ""}`;
  const currentData = data[getCurrentCode(code, currentLevel)];
  const nextData = data[getNextCode(code, currentLevel)] || {};

  const levelUpSkill = (event) => {
    levelUpFunction(code, event.shiftKey);
  }

  const levelDownSkill = (event) => {
    event.preventDefault();
    levelDownFunction(code, event.shiftKey);
  }

  return (
    <>
      <SkillDescription
        code={code}
        selectedLevel={selectedLevel}
        currentData={currentData}
        nextData={nextData}
      />

      <div className="skill" style={posStyle} data-tip data-for={code}>
        <div className={levelMinusClassName} onClick={levelDownSkill}>
          <FaMinus />
        </div>
        
        <div className="skill-icon-wrapper">
          <div className={effectClassName}>
            <img
              onClick={levelUpSkill}
              onContextMenu={levelDownSkill}
              src={`/static/img/skill_icons/${plannerClass}/${currentData.icon}`}
            />
          </div>
          <span className="level">{currentLevel}</span>
        </div>

        <div className={levelPlusClassName} onClick={levelUpSkill}>
          <FaPlus/>
        </div>

      </div>
    </>
  )
}

export default Skill;
export {
  getNextCode
}