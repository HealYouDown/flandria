/* eslint-disable no-unused-vars */
import React, { useEffect, useState } from 'react';
import Select from 'react-select';
import Card, { CardHeader } from '../shared/Card';
import useDidMountEffect from '../../useDidMountEffect';
import Hash from './Hash';
import {
  CLASSNAME_TO_INITIAL_POINTS, MAX_LEVEL_LAND, MAX_LEVEL_SEA, SHIFT_STATUS_INCREMENT,
  MAX_POINTS_LIMIT,
} from './constants';

const LabelValuePair = ({ label, value, labelClassname = '' }) => (
  <div className="flex justify-between text-gray-700 gap-x-2 dark:text-white">
    <span className={`font-semibold text-right ${labelClassname}`}>{label}</span>
    <span className="tabular-nums">{value}</span>
  </div>
);

const StatusButton = ({
  label, value, onIncrement, onDecrement,
}) => (
  <div className="flex items-center justify-between text-gray-900 dark:text-white">
    <span className="flex-grow">{label}</span>

    <div className="flex items-center gap-2">
      <button
        className="flex items-center justify-center w-4 h-4 font-extrabold text-center text-black bg-gray-200 border border-gray-500 rounded-md outline-none hover:bg-gray-300 focus-within:outline-none"
        type="button"
        onClick={onDecrement}
      >
        <span className="-mt-0.5">-</span>
      </button>
      <span>{value}</span>
      <button
        className="flex items-center justify-center w-4 h-4 font-extrabold text-center text-black bg-gray-200 border border-gray-500 rounded-md outline-none hover:bg-gray-300 focus-within:outline-none"
        type="button"
        onClick={onIncrement}
      >
        <span className="-mt-0.5 text-sm">+</span>
      </button>
    </div>
  </div>
);

const StatusPlanner = ({ classname, statusData, hash }) => {
  const [levelLand, setLevelLand] = useState(1);
  const [levelSea, setLevelSea] = useState(1);
  const [pointsLeft, setPointsLeft] = useState(0);
  const [pointsUsed, setPointsUsed] = useState(0);

  const [constitution, setConstitution] = useState(0);
  const [wisdom, setWisdom] = useState(0);
  const [intelligence, setIntelligence] = useState(0);
  const [will, setWill] = useState(0);
  const [dexterity, setDexterity] = useState(0);
  const [strength, setStrength] = useState(0);

  const [stats, setStats] = useState(null);

  const [unlimitedPoints, setUnlimitedPoints] = useState(false);

  const updatePoints = () => {
    let maxPoints = 0;

    // sea points
    maxPoints += (levelSea - 1);

    // land points
    if (levelLand <= 100) {
      maxPoints += (3 * levelLand);
    } else if (levelLand > 100 && levelLand < 105) {
      maxPoints += 3 * 100;
    } else if (levelLand === 105) {
      maxPoints += 3 * 100;
      maxPoints += 5; // on lv 105
    }

    // Calculate points used
    const initialPoints = CLASSNAME_TO_INITIAL_POINTS[classname];
    let pointsInvested = 0;
    pointsInvested += constitution - initialPoints.constitution;
    pointsInvested += wisdom - initialPoints.wisdom;
    pointsInvested += intelligence - initialPoints.intelligence;
    pointsInvested += will - initialPoints.will;
    pointsInvested += dexterity - initialPoints.dexterity;
    pointsInvested += strength - initialPoints.strength;

    setPointsUsed(pointsInvested);
    setPointsLeft(maxPoints - pointsInvested);
  };

  const updateHash = () => {
    const statusLevels = {
      constitution, wisdom, intelligence, will, dexterity, strength,
    };

    hash.updateStatusPlannerPart(levelLand, levelSea, unlimitedPoints, {
      constitution, wisdom, intelligence, will, dexterity, strength,
    });
  };

  const applyIncrementsToStats = (statsObj, increments) => {
    Object.keys(increments).forEach((key) => {
      // eslint-disable-next-line no-param-reassign
      statsObj[key] += increments[key];
    });

    return statsObj;
  };

  const incrementButtonClicked = (event, name, value, setFunction) => {
    let increment = 1;
    if (event.shiftKey) {
      if ((value + SHIFT_STATUS_INCREMENT) > MAX_POINTS_LIMIT) {
        increment = MAX_POINTS_LIMIT - value;
      } else {
        increment = SHIFT_STATUS_INCREMENT;
      }
    }

    if (!unlimitedPoints && pointsLeft < increment) {
      increment = pointsLeft;
    }

    if (value < MAX_POINTS_LIMIT) {
      setFunction(value + increment);
    }
  };

  const decrementButtonClicked = (event, name, value, setFunction) => {
    const initialPoints = CLASSNAME_TO_INITIAL_POINTS[classname];

    let decrement = 1;
    if (event.shiftKey) {
      if (initialPoints[name] > (value - SHIFT_STATUS_INCREMENT)) {
        decrement = value - initialPoints[name];
      } else {
        decrement = SHIFT_STATUS_INCREMENT;
      }
    }

    if (value > initialPoints[name]) {
      setFunction(value - decrement);
    }
  };

  const setInitialValues = () => {
    const initialPoints = CLASSNAME_TO_INITIAL_POINTS[classname];
    const hashValues = hash.getStatusPoints();
    console.log(hashValues);

    setConstitution(initialPoints.constitution + hashValues.constitution);
    setWisdom(initialPoints.wisdom + hashValues.wisdom);
    setIntelligence(initialPoints.intelligence + hashValues.intelligence);
    setWill(initialPoints.will + hashValues.will);
    setDexterity(initialPoints.dexterity + hashValues.dexterity);
    setStrength(initialPoints.strength + hashValues.strength);
  };

  useEffect(() => {
    // Load level etc. from hash
    const statusInformation = hash.getStatusInformation();
    setLevelLand(statusInformation.levelLand);
    setLevelSea(statusInformation.levelSea);
    setUnlimitedPoints(statusInformation.unlimitedPoints);
    // Set initial skill values
    setInitialValues();
  }, []);

  const resetToZero = () => {
    const initialPoints = CLASSNAME_TO_INITIAL_POINTS[classname];

    setConstitution(initialPoints.constitution);
    setWisdom(initialPoints.wisdom);
    setIntelligence(initialPoints.intelligence);
    setWill(initialPoints.will);
    setDexterity(initialPoints.dexterity);
    setStrength(initialPoints.strength);
  };

  useDidMountEffect(() => {
    let statsObject = { ...statusData.level.filter((o) => o.level === levelLand)[0] };

    // Con
    statsObject = applyIncrementsToStats(
      statsObject,
      statusData.constitution.filter((o) => o.level === constitution)[0],
    );

    // Wis
    statsObject = applyIncrementsToStats(
      statsObject,
      statusData.wisdom.filter((o) => o.level === wisdom)[0],
    );

    // Int
    statsObject = applyIncrementsToStats(
      statsObject,
      statusData.intelligence.filter((o) => o.level === intelligence)[0],
    );

    // Will
    statsObject = applyIncrementsToStats(
      statsObject,
      statusData.will.filter((o) => o.level === will)[0],
    );

    // Dexterity
    statsObject = applyIncrementsToStats(
      statsObject,
      statusData.dexterity.filter((o) => o.level === dexterity)[0],
    );

    // Str
    statsObject = applyIncrementsToStats(
      statsObject,
      statusData.strength.filter((o) => o.level === strength)[0],
    );
    setStats(statsObject);
    updatePoints();
    updateHash();

    if (!unlimitedPoints && pointsLeft < 0) {
      resetToZero();
    }
  }, [
    constitution, wisdom, intelligence, will, dexterity, strength, levelLand, levelSea,
    unlimitedPoints,
  ]);

  if (!stats) return null;

  const levelLandOptions = [];
  for (let i = 1; i <= MAX_LEVEL_LAND; i += 1) {
    levelLandOptions.push({
      label: i, value: i,
    });
  }

  const levelSeaOptions = [];
  for (let i = 1; i <= MAX_LEVEL_SEA; i += 1) {
    levelSeaOptions.push({
      label: i, value: i,
    });
  }

  return (
    <Card
      className="md:max-w-md h-min-content"
      header={(
        <CardHeader>
          <div className="grid grid-cols-1 gap-2 md:grid-cols-2">
            <div>
              <span className="font-semibold text-gray-700 dark:text-white">Level Land</span>
              <Select
                classNamePrefix="react-select"
                options={levelLandOptions}
                value={levelLandOptions.filter((opt) => opt.value === levelLand)}
                onChange={(opt) => setLevelLand(opt.value)}
              />
            </div>
            <div>
              <span className="font-semibold text-gray-700 dark:text-white">Level Sea</span>
              <Select
                classNamePrefix="react-select"
                options={levelSeaOptions}
                value={levelSeaOptions.filter((opt) => opt.value === levelSea)}
                onChange={(opt) => setLevelSea(opt.value)}
              />
            </div>
          </div>
          <p className="mt-2 text-sm leading-none text-gray-500 dark:text-white dark:text-opacity-70">
            Results may be off by up to 1-2.
            Stats from skills are
            {' '}
            <b>not</b>
            {' '}
            accounted for.
          </p>
        </CardHeader>
      )}
    >
      <div className="flex flex-col gap-5 px-2 py-4 divide-y divide-gray-200 sm:px-4 lg:px-6 dark:divide-dark-4">
        <div className="flex flex-row justify-around text-gray-700 dark:text-white">
          <span>
            Points Left:
            {' '}
            {unlimitedPoints ? '/' : pointsLeft}
          </span>
          <span>
            Points Used:
            {' '}
            {pointsUsed}
          </span>
          <label htmlFor="unlimited-points-checkbox" className="flex items-center gap-1 select-none">
            <input
              id="unlimited-points-checkbox"
              type="checkbox"
              checked={unlimitedPoints}
              onChange={(e) => {
                setInitialValues();
                setUnlimitedPoints(e.target.checked);
              }}
            />
            Unlimited Points
          </label>
        </div>
        <div className="grid grid-cols-1 pt-2 md:grid-cols-2 gap-x-8">
          <StatusButton
            label="Strength"
            value={strength}
            onIncrement={(e) => incrementButtonClicked(e, 'strength', strength, setStrength)}
            onDecrement={(e) => decrementButtonClicked(e, 'strength', strength, setStrength)}
          />
          <StatusButton
            label="Intelligence"
            value={intelligence}
            onIncrement={(e) => incrementButtonClicked(e, 'intelligence', intelligence, setIntelligence)}
            onDecrement={(e) => decrementButtonClicked(e, 'intelligence', intelligence, setIntelligence)}
          />
          <StatusButton
            label="Dexterity"
            value={dexterity}
            onIncrement={(e) => incrementButtonClicked(e, 'dexterity', dexterity, setDexterity)}
            onDecrement={(e) => decrementButtonClicked(e, 'dexterity', dexterity, setDexterity)}
          />
          <StatusButton
            label="Wisdom"
            value={wisdom}
            onIncrement={(e) => incrementButtonClicked(e, 'wisdom', wisdom, setWisdom)}
            onDecrement={(e) => decrementButtonClicked(e, 'wisdom', wisdom, setWisdom)}
          />
          <StatusButton
            label="Constitution"
            value={constitution}
            onIncrement={(e) => incrementButtonClicked(e, 'constitution', constitution, setConstitution)}
            onDecrement={(e) => decrementButtonClicked(e, 'constitution', constitution, setConstitution)}
          />
          <StatusButton
            label="Will"
            value={will}
            onIncrement={(e) => incrementButtonClicked(e, 'will', will, setWill)}
            onDecrement={(e) => decrementButtonClicked(e, 'will', will, setWill)}
          />
          <div className="flex justify-end col-span-2 mt-2">
            <span className="text-xs text-gray-500 dark:text-white dark:text-opacity-70">
              Click ± 1. Shift-Click ± 15.
            </span>
          </div>
        </div>
        <div className="grid grid-cols-1 pt-2 md:grid-cols-2 gap-x-6 gap-y-2">
          <div>
            <LabelValuePair label="HP" labelClassname="text-red-500 dark:text-red-400" value={Number(stats.max_hp).toLocaleString()} />
            <LabelValuePair label="MP" labelClassname="text-blue-500 dark:text-blue-400" value={Number(stats.max_mp).toLocaleString()} />
            <LabelValuePair label="Avoidance" value={Number(stats.avoidance).toLocaleString()} />
          </div>
          <div>
            <LabelValuePair label="Melee Akt." value={`${Number(stats.melee_min_attack).toLocaleString()}~${Number(stats.melee_max_attack).toLocaleString()}`} />
            <LabelValuePair label="Melee Hit" value={Number(stats.melee_hitrate).toLocaleString()} />
            <LabelValuePair label="Melee Crit" value={Number(stats.melee_critical_rate).toLocaleString()} />
          </div>
          <div>
            <LabelValuePair label="Range Akt." value={`${Number(stats.range_min_attack).toLocaleString()}~${Number(stats.range_max_attack).toLocaleString()}`} />
            <LabelValuePair label="Range Hit" value={Number(stats.range_hitrate).toLocaleString()} />
            <LabelValuePair label="Range Crit" value={Number(stats.range_critical_rate).toLocaleString()} />
          </div>
          <div>
            <LabelValuePair label="Magic Akt." value={`${Number(stats.magic_min_attack).toLocaleString()}~${Number(stats.magic_max_attack).toLocaleString()}`} />
            <LabelValuePair label="Magic Hit" value={Number(stats.magic_hitrate).toLocaleString()} />
            <LabelValuePair label="Magic Crit" value={Number(stats.magic_critical_rate).toLocaleString()} />
          </div>
        </div>
      </div>
    </Card>
  );
};

export default StatusPlanner;
export {
  CLASSNAME_TO_INITIAL_POINTS,
};
