import React from 'react';
import { GiMagicSwirl, GiEmptyHourglass, GiHighShot } from 'react-icons/gi';
import ReactTooltip from 'react-tooltip';
import { formatTextLinebreaks } from '../../../../helpers';
import Card, { CardHeader, CardHeaderTitle } from '../../../shared/Card';
import Icon from '../../../shared/Icon';

const SkillDataAttribute = ({
  icon, text, tooltip,
}) => (
  <>
    <div data-tip={tooltip} className="cursor-default flex gap-x-0.5 items-center text-gray-700 dark:text-white">
      {icon}
      <span>{text}</span>
    </div>
  </>
);

const Skill = ({ skill }) => (
  <div className="flex flex-row px-4 py-2">
    <Icon tablename="skill" icon={skill.icon} className="mr-1.5 w-10 h-10" />
    <div className="flex flex-col flex-grow">
      <div className="flex items-center justify-between gap-16">
        <span className="leading-none text-gray-700 whitespace-pre-wrap dark:text-white">
          {skill.name}
        </span>
        <div className="flex justify-end gap-x-2">
          <SkillDataAttribute
            key="level"
            icon={<GiHighShot />}
            text={`${skill.required_level_land}`}
            tooltip="Required Level"
          />
          <SkillDataAttribute
            key="casttime"
            icon={<GiMagicSwirl />}
            text={`${skill.cast_time}s`}
            tooltip="Cast Time"
          />
          <SkillDataAttribute
            key="cooldown"
            icon={<GiEmptyHourglass />}
            text={`${skill.cooldown}s`}
            tooltip="Cooldown"
          />
          <ReactTooltip effect="solid" />
        </div>
      </div>
      <span className="text-sm leading-5 text-gray-500 whitespace-pre-line dark:text-white dark:text-opacity-70">
        {formatTextLinebreaks(skill.description)}
      </span>
    </div>
  </div>
);

const SkillWidget = ({ skills }) => {
  if (skills.length === 0) return null;

  return (
    <Card
      header={(
        <CardHeader>
          <CardHeaderTitle>Skills</CardHeaderTitle>
        </CardHeader>
        )}
    >
      <div className="divide-y divide-gray-200 dark:divide-dark-4">
        {skills.map((skill) => <Skill key={skill.code} skill={skill} />)}
      </div>
    </Card>
  );
};

export default SkillWidget;
