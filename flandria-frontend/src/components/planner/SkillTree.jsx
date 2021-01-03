import React from 'react';
import Select from 'react-select';
import { toBlob } from 'dom-to-image';
import { HiDownload } from 'react-icons/hi';
// This has to be imported, but is not used directly.
// eslint-disable-next-line no-unused-vars
import { saveAs } from 'file-saver';
import Card, { CardHeader } from '../shared/Card';
import { getImagePath } from '../../helpers';
import SkillObject from './SkillObject';
import Skill from './Skill';

const classSelectOptions = {
  explorer: [
    { label: 'Explorer', value: 'E' },
    { label: 'Sniper', value: 'H' },
    { label: 'Excavator', value: 'B' },
  ],
  saint: [
    { label: 'Saint', value: 'S' },
    { label: 'Priest', value: 'P' },
    { label: 'Shaman', value: 'A' },
  ],
  noble: [
    { label: 'Noble', value: 'N' },
    { label: 'Court Magician', value: 'M' },
    { label: 'Magic Knight', value: 'K' },
  ],
  mercenary: [
    { label: 'Mercenary', value: 'W' },
    { label: 'Gladiator', value: 'G' },
    { label: 'Guardian Swordsman', value: 'D' },
  ],
  ship: [],
};

class SkillTree extends React.Component {
  constructor(props) {
    super(props);

    this.onSkillLevelDownRequest = this.onSkillLevelDownRequest.bind(this);
    this.onSkillLevelUpRequest = this.onSkillLevelUpRequest.bind(this);

    this.state = this.getDefaultState();
    this.classOptions = null;
    this.levelOptions = null;

    this.plannerDivRef = React.createRef();
  }

  componentDidMount() {
    // Once the component is mounted, fetch the planner data
    // and init all other stuff
    this.init();
  }

  componentDidUpdate(prevProps) {
    // If any props changed, check if classname was change as well
    // if so, re-initalize everything with the new classname
    const { classname } = this.props;
    if (classname !== prevProps.classname) {
      // eslint-disable-next-line react/no-did-update-set-state
      this.setState(this.getDefaultState());
      this.init();
    }
  }

  onClassChange(newSelectedClass) {
    const { selectedLevel } = this.state;

    // If the new class is a CC class and level is < 40, do not update class
    if (!['W', 'E', 'N', 'S'].includes(newSelectedClass) && selectedLevel < 40) {
      return null;
    }

    // Update class
    this.setState({ selectedClass: newSelectedClass }, () => {
      this.updateAllowedSkills();
      this.updatePoints();
      this.updateHashBasedOnState();
    });

    return null;
  }

  onLevelChange(newSelectedLevel) {
    const { selectedLevel, selectedClass } = this.state;
    if (newSelectedLevel < selectedLevel) {
      // Reset skills because the new level is now smaller
      this.resetSkills(false);
    }

    // Reset class to base class if < 40
    const newSelectedClass = (newSelectedLevel < 40) ? this.classOptions[0].value : selectedClass;

    this.setState({
      selectedLevel: newSelectedLevel,
      selectedClass: newSelectedClass,
    }, () => {
      this.updateAllowedSkills();
      this.updatePoints();
      this.updateHashBasedOnState();
    });
  }

  onSkillLevelUpRequest(skillCode, shiftKeyPressed) {
    // Check if skill level up requirements are
    // fullfilled on the real state object.
    // If they are, copy state and update it.
    const { skillObjects, selectedLevel } = this.state;
    let { pointsLeft } = this.state;

    if (skillObjects[skillCode].levelUpRequirementsFullfilled(selectedLevel, pointsLeft)) {
      const skillObjectsCopy = { ...skillObjects };
      const skillObj = skillObjectsCopy[skillCode];

      if (shiftKeyPressed) {
        // Increase as often as it can do
        for (let i = 0; i <= 15; i += 1) {
          if (skillObj.levelUpRequirementsFullfilled(selectedLevel, pointsLeft)) {
            skillObj.skillLevel += 1;
            pointsLeft -= 1;
          }
        }
      } else {
        skillObj.skillLevel += 1;
      }

      this.setState({ skillObjects: skillObjectsCopy }, () => {
        this.updateAllowedSkills();
        this.updatePoints();
        this.updateHashBasedOnState();
      });
    }
  }

  onSkillLevelDownRequest(skillCode, isShift = false) {
    const { skillObjects } = this.state;
    const skillObjectsCopy = { ...skillObjects };
    const skillObj = skillObjectsCopy[skillCode];

    // A level 0 skill is no longer able to be decreased,
    // kinda obvious
    if (skillObj.skillLevel > 0) {
      // Decrase level by one

      if (isShift) {
        skillObj.skillLevel = 0;
      } else {
        skillObj.skillLevel -= 1;
      }

      // If skill level was reduced to 0, disable all skills that relied
      // on it
      if (skillObj.skillLevel === 0) {
        this.getReliedOnSkillCodes(skillObj.skillCode).forEach((reliedOnSkillCode) => {
          const reliedOnSkillObj = skillObjectsCopy[reliedOnSkillCode];
          reliedOnSkillObj.skillLevel = 0;
          reliedOnSkillObj.allowed = false;
        });
      }

      this.setState({ skillObjects: skillObjectsCopy }, () => {
        this.updatePoints();
        this.updateHashBasedOnState();
      });
    }
  }

  // eslint-disable-next-line class-methods-use-this
  getDefaultState() {
    return ({
      selectedLevel: null,
      selectedClass: null,

      pointsLeft: 0,
      pointsUsed: 0,

      skillObjects: {},
      preparing: true,
    });
  }

  getReliedOnSkillCodes(skillCode) {
    const { skillObjects } = this.state;
    const childrenSkillCodes = [];

    Object.values(skillObjects).forEach((skillObj) => {
      if (
        !childrenSkillCodes.includes(skillObj.skillCode)
        && skillObj.getRequiredSkills().includes(skillCode)
      ) {
        childrenSkillCodes.push(skillObj.skillCode);
        childrenSkillCodes.push(...this.getReliedOnSkillCodes(skillObj.skillCode));
      }
    });

    return childrenSkillCodes;
  }

  resetSkills(updateAllowedSkills = false) {
    const { skillObjects } = this.state;

    // Clone skill objects as stated should not be changed directly
    const skillObjectsCopy = { ...skillObjects };
    Object.values(skillObjectsCopy).forEach((skillObj) => skillObj.reset());

    this.setState({
      skillObjects: skillObjectsCopy,
    }, () => {
      if (updateAllowedSkills) {
        this.updateAllowedSkills();
        this.updatePoints();
        this.updateHashBasedOnState();
      }
    });
  }

  updateHashBasedOnState() {
    const {
      selectedLevel, selectedClass, skillObjects,
    } = this.state;
    const { classname, hash } = this.props;

    let classIndex = 0;
    if (classname !== 'ship') {
      classIndex = this.classOptions.indexOf(this.classOptions.filter(
        (opt) => opt.value === selectedClass,
      )[0]);
    }

    const skillLevels = [];
    hash.skillCodes.forEach((skillCode) => {
      skillLevels.push(skillObjects[skillCode].skillLevel);
    });

    hash.updateSkillTreePart(
      selectedLevel,
      classIndex,
      skillLevels,
    );
  }

  init() {
    const { skillData, classname, hash } = this.props;

    // Set class options
    this.classOptions = classSelectOptions[classname];

    // set Level options
    const maxCharacterLevel = (classname === 'ship') ? 99 : 105;
    this.levelOptions = [];
    for (let i = 1; i <= maxCharacterLevel; i += 1) {
      this.levelOptions.push({
        label: i, value: i,
      });
    }

    // Create skill objects from data
    const initialSkillObjects = {};
    Object.keys(skillData).forEach((skillCode) => {
      initialSkillObjects[skillCode] = new SkillObject(
        classname,
        skillCode,
        skillData[skillCode],
      );
    });

    Object.keys(initialSkillObjects).forEach((skillCode) => {
      const skillObj = initialSkillObjects[skillCode];
      skillObj.skillLevel = hash.getSkillLevel(skillCode);
    });

    this.setState({
      preparing: false,
      skillObjects: initialSkillObjects,
      selectedLevel: hash.getCharacterLevel(),
      selectedClass: (classname === 'ship') ? 0 : this.classOptions[hash.getClassIndex()].value,
    }, () => {
      this.updateAllowedSkills();
      this.updatePoints();
    });
  }

  updateAllowedSkills() {
    // Go through all skills and check if conditions have
    // changed and a skill is now allowed or not allowed at all.
    const {
      skillObjects, selectedLevel, selectedClass,
    } = this.state;
    const { classname } = this.props;

    // Clone skill objects as stated should not be changed directly
    const skillObjectsCopy = { ...skillObjects };

    Object.keys(skillObjectsCopy).forEach((skillCode) => {
      const skillObj = skillObjectsCopy[skillCode];
      const { baseSkill } = skillObj;

      // Check conditions
      // Returns (breaks the current iteration) if a condition
      // is not met.
      // At the end, if all checks passed, a skill will be set to
      // allowed.

      // Level
      const skillLevel = (
        (classname === 'ship')
          ? baseSkill.required_level_sea
          : baseSkill.required_level_land);
      if (skillLevel > selectedLevel) {
        return;
      }

      // Ship class can skill each skill, no matter the class.
      if (classname !== 'ship') {
        const baseClassNames = ['W', 'E', 'N', 'S'];

        const requiredClassesLand = skillObj.baseSkill.class_land.split('');
        const isCCSkill = !(requiredClassesLand.some(
          (classLetter) => baseClassNames.includes(classLetter),
        ));

        if (isCCSkill && !(requiredClassesLand).includes(selectedClass)) {
          // CC Skill does not have the right class, so it is reset
          skillObj.skillLevel = 0;
          skillObj.allowed = false;
          return;
        }
      }

      // Check if required parent skills are skilled
      let parentsSkillAreSkilled = true;
      skillObj.getRequiredSkills().forEach((requiredSkillCode) => {
        if (skillObjectsCopy[requiredSkillCode].skillLevel === 0) {
          parentsSkillAreSkilled = false;
        }
      });

      if (!parentsSkillAreSkilled) {
        return;
      }

      skillObj.allowed = true;
    });

    this.setState({ skillObjects: skillObjectsCopy });
  }

  updatePoints() {
    const { skillObjects, selectedLevel } = this.state;

    // Calcualte max points
    let pointsMax = 0;
    if (selectedLevel <= 100) {
      pointsMax = selectedLevel;
    } else if (selectedLevel <= 104) {
      pointsMax = 100;
    } else if (selectedLevel === 105) {
      pointsMax = 101;
    }

    // Calculate points already used
    let pointsUsed = 0;
    Object.values(skillObjects).forEach((skillObj) => {
      pointsUsed += skillObj.skillLevel;
    });

    // Points left
    const pointsLeft = pointsMax - pointsUsed;

    this.setState({ pointsLeft, pointsUsed });
  }

  saveAsImage() {
    const { classname } = this.props;

    if (this.plannerDivRef.current) {
      toBlob(this.plannerDivRef.current,
        {
          filter: (node) => {
            if (node.id && node.id.includes('excluded-in-image')) {
              return false;
            }
            return true;
          },
        }).then((blob) => {
        window.saveAs(blob, `skilltree-${classname}`);
      });
    }
  }

  render() {
    const {
      skillObjects, selectedClass, selectedLevel, pointsLeft, pointsUsed, preparing,
    } = this.state;
    const { classname } = this.props;

    const skilltreeSize = { width: '448px', height: '502px' };

    if (preparing) return null;

    return (
      <Card
        refObject={this.plannerDivRef}
        className="flex-grow-0 overflow-x-auto"
        header={(
          <CardHeader>
            <div className={`grid ${classname === 'ship' ? 'grid-cols-1' : 'grid-cols-2'} gap-3`}>
              {classname !== 'ship' && (
              <Select
                classNamePrefix="react-select"
                className="flex-grow"
                options={this.classOptions}
                value={this.classOptions.filter((opt) => opt.value === selectedClass)}
                onChange={(opt) => this.onClassChange(opt.value)}
              />
              )}
              <Select
                classNamePrefix="react-select"
                className="flex-grow"
                options={this.levelOptions}
                value={this.levelOptions.filter((opt) => opt.value === selectedLevel)}
                onChange={(opt) => this.onLevelChange(opt.value)}
              />
            </div>
            <div className="flex items-center justify-center col-span-2 gap-6 mt-2">
              <span className="text-gray-700 dark:text-white">
                Points Left:
                {' '}
                <span className="tabular-nums">
                  {pointsLeft}
                </span>
              </span>
              <span className="text-gray-700 dark:text-white">
                Points Used:
                {' '}
                <span className="tabular-nums">
                  {pointsUsed}
                </span>
              </span>
              <button
                onClick={() => this.saveAsImage()}
                type="button"
                id="excluded-in-image"
                className="flex items-center gap-1 px-2 py-1 text-white bg-green-500 rounded-md hover:bg-green-600"
              >
                <HiDownload className="w-4 h-4" />
                Download
              </button>
            </div>
          </CardHeader>
      )}
      >
        <div className="px-10 py-3 overflow-x-auto">
          <div
            className="relative rounded-lg select-none"
            style={{ ...skilltreeSize, backgroundImage: `url(${getImagePath(`planner/${classname}.png`)})` }}
          >
            {Object.values(skillObjects).map((skillObj) => (
              <Skill
                classname={classname}
                skillObj={skillObj}
                selectedLevel={selectedLevel}
                onLevelDownRequest={this.onSkillLevelDownRequest}
                onLevelUpRequest={this.onSkillLevelUpRequest}
              />
            ))}
            <span className="absolute bottom-0 right-0 text-xs text-gray-500 dark:text-white dark:text-opacity-70">
              Click ± 1. Shift-Click Max.
            </span>
          </div>
        </div>
      </Card>
    );
  }
}

export default SkillTree;
