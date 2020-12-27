import React from 'react';
import ReactTooltip from 'react-tooltip';
import {
  formatTextLinebreaks,
  getImagePath, resolveLandClassNames, resolveSeaClassNames, resolveWeaponTypeToName,
} from '../../helpers';

const SkillDataPair = ({ label, value, red = false }) => (
  <div className="flex items-center justify-between">
    <span className="text-sm font-medium leading-none text-white">{label}</span>
    <span className={`${red ? 'text-red-600' : 'text-white text-opacity-70'} text-sm`}>{value}</span>
  </div>
);

const SkillDataInfo = ({ classname, currentLevel, skillData }) => {
  const requiredLevel = (
    (classname === 'ship')
      ? skillData.required_level_sea
      : skillData.required_level_land);

  return (
    <div className="flex flex-col">
      <div className="grid grid-cols-2 gap-x-3">
        <SkillDataPair
          label="Req. Level"
          value={requiredLevel}
          red={requiredLevel > currentLevel}
        />
        <SkillDataPair
          label="Cooldown"
          value={skillData.cooldown ? `${skillData.cooldown}s` : '0s'}
        />
        <SkillDataPair
          label="MP"
          value={skillData.mana_cost}
        />
        <SkillDataPair
          label="Cast Time"
          value={skillData.cast_time ? `${skillData.cast_time}s` : '0s'}
        />
        <SkillDataPair
          label="Cast Range"
          value={skillData.cast_distance ? `${skillData.cast_distance}m` : '/'}
        />
        <SkillDataPair
          label="Effect Range"
          value={skillData.effect_range ? `${skillData.effect_range}m` : '/'}
        />
      </div>
      <p className="mt-1 leading-none text-white text-opacity-70">
        {formatTextLinebreaks(skillData.description)}
      </p>
    </div>
  );
};

const Skill = ({
  classname, skillObj, selectedLevel, onLevelUpRequest, onLevelDownRequest,
}) => {
  const skillCode = skillObj.skillCode;

  let skillStyle = '';
  if (!skillObj.allowed) {
    skillStyle = 'skill-disabled';
  } else if (skillObj.allowed && skillObj.skillLevel === 0) {
    skillStyle = 'skill-not-skilled';
  }

  const position = skillObj.getPosition();

  return (
    <>
      <button
        className="absolute md:hidden"
        style={{ left: `${position.left - 12 - 1}px`, top: `${position.top}px` }}
        type="button"
        onClick={() => onLevelDownRequest(skillCode)}
        id="excluded-from-image"
      >
        <img
          height={32}
          className="skill-not-skilled hover:reset-filter"
          src={getImagePath('planner/minus_button.png')}
          alt="plus button"
          id="excluded-from-image"
        />
      </button>
      <button
        className="absolute md:hidden"
        style={{ left: `${position.left + 32 + 1}px`, top: `${position.top}px` }}
        type="button"
        onClick={() => onLevelUpRequest(skillCode)}
        id="excluded-from-image"
      >
        <img
          height={32}
          className="skill-not-skilled hover:reset-filter"
          src={getImagePath('planner/plus_button.png')}
          alt="plus button"
          id="excluded-from-image"
        />
      </button>

      <div
        data-tip
        data-for={skillCode}
        key={skillCode}
        role="button"
        className="absolute"
        style={{ left: `${position.left}px`, top: `${position.top}px` }}
        onClick={(e) => onLevelUpRequest(skillCode, e.shiftKey)}
        onContextMenu={(e) => {
          e.preventDefault();
          onLevelDownRequest(skillCode, e.shiftKey);
        }}
        aria-hidden
      >
        <div
          className="relative"
        >
          <img
            width={32}
            height={32}
            src={getImagePath(`skill_icons_upscaled/${skillObj.baseSkill.icon}`)}
            alt="skill icon"
            className={`${skillStyle} rounded-md`}
            id="included-in-image"
          />
          <span
            className="absolute bottom-0 text-sm text-white bg-black tabular-nums opacity-70 rounded-bl-md px-0.5 rounded-tr-md"
            id="included-in-image"
          >
            {skillObj.skillLevel}
          </span>
        </div>
      </div>
      <div id="excluded-in-image">
        <ReactTooltip
          id={`${skillCode}`}
          className="w-80"
          effect="solid"
          place="right"
          clickable
          type="dark"
          delayHide={50}
          delayShow={150}
        >
          <div className="flex flex-col gap-3 divide-y divide-white">
            <div className="flex justify-between">
              <div className="flex-col gap-2">
                <h2 className="text-base text-green-500">{skillObj.baseSkill.name}</h2>
                <p className="text-xs leading-none text-white opacity-70">
                  {((classname === 'ship')
                    ? resolveSeaClassNames(skillObj.baseSkill.class_sea)
                    : resolveLandClassNames(skillObj.baseSkill.class_land))}
                </p>
                <p className="text-xs leading-none text-white opacity-70">
                  {resolveWeaponTypeToName(skillObj.baseSkill.required_weapons)}
                </p>
              </div>
              <span className="text-base text-yellow-600">
                {skillObj.skillLevel}
                /
                {skillObj.baseSkill.max_level}
              </span>
            </div>

            {skillObj.skillLevel > 0 && (
            <SkillDataInfo
              classname={classname}
              currentLevel={selectedLevel}
              skillData={skillObj.getSkillForCurrentLevel()}
            />
            )}
            {(skillObj.skillLevel !== skillObj.baseSkill.max_level) && (
            <div>
              <span className="block py-1 text-center text-white">
                Next Level: (
                {skillObj.skillLevel + 1}
                )
              </span>
              <SkillDataInfo
                classname={classname}
                currentLevel={selectedLevel}
                skillData={skillObj.getSkillForNextLevel()}
              />
            </div>
            )}
          </div>
        </ReactTooltip>
      </div>
    </>
  );
};

export default Skill;
