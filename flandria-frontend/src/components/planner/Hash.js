/*
A hash consists of 3 parts seperated with a .

Level + Class:
  <level>.<class_index>

Skills part:
  <skill_code_1>:<skill_code_2>........

Stat Points part:
    <level_l>:<level_s>:<unlimited>.<con>:<wis>:....

Example: 105:2.1:2:5:1:0:0:0:51:4:3
*/
import { CLASSNAME_TO_INITIAL_POINTS } from './constants';

class Hash {
  constructor(classname, skillCodes) {
    this.classname = classname;

    this.skillCodes = skillCodes;

    // Get current hash and replace # in front
    this.hash = window.location.hash.replace('#', '');

    this.partDelimiter = '.';
    this.valueDelimiter = ':';

    this.statusIndexToName = {
      0: 'strength',
      1: 'constitution',
      2: 'will',
      3: 'dexterity',
      4: 'wisdom',
      5: 'intelligence',
    };

    this.statusNameToIndex = {
      strength: 0,
      constitution: 1,
      will: 2,
      dexterity: 3,
      wisdom: 4,
      intelligence: 5,
    };
  }

  updateHashInUrl() {
    window.location.hash = `#${this.hash}`;
  }

  updateSkillTreePart(level, classIndex, skillLevels) {
    const parts = [];
    // Level Part
    parts.push([level, classIndex].join(this.valueDelimiter));
    // Skill Part
    parts.push(skillLevels.join(this.valueDelimiter));
    // Stat Level Part
    parts.push(this.getPart(2));
    // Stat Points Part
    parts.push(this.getPart(3));

    this.hash = parts.join(this.partDelimiter);
    this.updateHashInUrl();
  }

  getPart(num) {
    return this.hash.split(this.partDelimiter)[num];
  }

  exists() {
    /* Returns true if hash exists, false if not */
    // Note: 5 is a random chosen value
    return this.hash.length > 5;
  }

  setDefaultHash() {
    const parts = [];
    // Level Part
    parts.push(`1${this.valueDelimiter}0`);
    // Skill Part
    parts.push(new Array(this.skillCodes.length).fill('0').join(this.valueDelimiter));
    // Stat Level Part
    parts.push(`1${this.valueDelimiter}1${this.valueDelimiter}0`);
    // Stat points part
    parts.push(new Array(6).fill('0').join(this.valueDelimiter));

    this.hash = parts.join(this.partDelimiter);
    this.updateHashInUrl();
  }

  getCharacterLevel() {
    const levelClassPart = this.getPart(0);
    const [level] = levelClassPart.split(this.valueDelimiter);

    return parseInt(level, 10);
  }

  getClassIndex() {
    const levelClassPart = this.getPart(0);
    const [, classIndex] = levelClassPart.split(this.valueDelimiter);

    return parseInt(classIndex, 10);
  }

  getSkillLevel(skillCode) {
    const skillPart = this.getPart(1);
    const skillIndex = this.skillCodes.indexOf(skillCode);
    const skillLevels = skillPart.split(this.valueDelimiter);

    return parseInt(skillLevels[skillIndex], 10);
  }

  getStatusInformation() {
    const statusInformationPart = this.getPart(2);
    const partSplitted = statusInformationPart.split(this.valueDelimiter);

    return {
      levelLand: parseInt(partSplitted[0], 10),
      levelSea: parseInt(partSplitted[1], 10),
      unlimitedPoints: Boolean(parseInt(partSplitted[2], 10)),
    };
  }

  getStatusPoints() {
    const statusPointsPart = this.getPart(3);
    const result = {};

    statusPointsPart.split(this.valueDelimiter).forEach((valueString, index) => {
      const value = parseInt(valueString, 10);
      result[this.statusIndexToName[index]] = value;
    });

    return result;
  }

  updateStatusPlannerPart(levelLand, levelSea, unlimited, statusPoints) {
    const parts = [this.getPart(0), this.getPart(1)];

    // Status information part
    parts.push([levelLand, levelSea, unlimited ? 1 : 0].join(this.valueDelimiter));

    // Status points part
    const partSplitted = [];

    Object.keys(this.statusNameToIndex).forEach((key) => {
      partSplitted.push(statusPoints[key] - CLASSNAME_TO_INITIAL_POINTS[this.classname][key]);
    });

    parts.push(partSplitted.join(this.valueDelimiter));

    this.hash = parts.join(this.partDelimiter);
    this.updateHashInUrl();
  }
}

export default Hash;
