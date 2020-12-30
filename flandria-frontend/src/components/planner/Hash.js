/*
A hash consists of 3 parts seperated with a .

Level + Class:
  <level>.<class_index>

Skills part:
  <skill_code_1>:<skill_code_2>........

Stat Points part:
    <con>:<wis>:....

Example: 105:2.1:2:5:1:0:0:0:51:4:3
*/

class Hash {
  constructor(classname, skillCodes) {
    this.classname = classname;
    // Sort skill codes so that they are always positioned
    // the same in the array.
    this.skillCodes = skillCodes;

    // Get current hash and replace # in front
    this.hash = window.location.hash.replace('#', '');

    this.partDelimiter = '.';
    this.valueDelimiter = ':';
  }

  updateHashInUrl() {
    window.location.hash = `#${this.hash}`;
  }

  updateCompleteHash(level, classIndex, skillLevels, statPoints) {
    const parts = [];
    // Level Part
    parts.push([level, classIndex].join(this.valueDelimiter));
    // Skill Part
    parts.push(skillLevels.join(this.valueDelimiter));
    // Stat Part
    parts.push(statPoints.join(this.valueDelimiter));

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
    // Stat Part
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
}

export default Hash;
