import React from "react";
import ReactTooltip from "react-tooltip";

import "./SkillDescription.css";

const Stats = ({selectedLevel, data}) => {
  const levelClass = selectedLevel >= data.required_level ? "" : "not-allowed";

  return (
    <>
      <div className="skill-description-stats">
        <div>
          <span>Req. Level</span>
          <span className={levelClass}>{data.required_level}</span>
        </div>
        <div>
          <span>Mp</span>
          <span>{data.mana_consumption}</span>
        </div>
        <div>
          <span>Cooldown</span>
          <span>{data.cooldown/1000}s</span>
        </div>
      </div>
      <div className="skill-description-text">
        {data.description.split("\\n").map((desc, i) => {
          return (
            <span key={i}>
              {desc}
              <br />
            </span>
          )
        })}
      </div>
    </>

  )
}

const SkillDescription = ({code, selectedLevel, currentData, nextData}) => {
  const name = currentData.name;

  const currentLevel = currentData.skill_level;
  const maxLevel = currentData.max_level;
  const nextLevel = nextData.skill_level || 0;

  return (
    <ReactTooltip 
      id={code}
      effect="solid"
      place="right"
      clickable={true}
      multiline={true}
      delayHide={50}
      delayShow={150}
      className="skill-description"
    >
      <div className="skill-description-header">
        <span className="skill-name">{name}</span>
        <span className="skill-level">{currentLevel}/{maxLevel}</span>
      </div>
      <div className="skill-description-sub-header">
        <span>{currentData.class_land}</span>
      </div>
      <hr className="skill-description-divider" />
      {currentLevel >= 1 && (
        <>
          <Stats selectedLevel={selectedLevel} data={currentData} />
          {currentLevel != maxLevel && (
            <hr className="skill-description-divider" />
          )}
        </>
      )}
      {currentLevel != maxLevel && (
        <>
          <span className="next-level">Next Level ({nextLevel}):</span>
          <Stats selectedLevel={selectedLevel} data={nextData} />
        </>
      )} 
    </ReactTooltip>
  )
}

export default SkillDescription;