/*
A hash consists of 2 parts seperated with a .

Level + Class part:
  <level>.<class_index>

Skills part:
  <skill_code_1>:<skill_code_2>........

Example: 105:2.1:2:5:1:0:0:0:51:4:3
*/

class Hash {
  constructor(plannerClass, skillCodes) {
    this.plannerClass = plannerClass;
    this.skillCodes = skillCodes;
    this.hash = location.hash.replace("#", "");
  }

  exists() {
    /* Returns true if hash exists, false if not */
    return this.hash.length >= 5;
  }

  getLevelFromHash() {
    /* Returns the level from the hash */
    const levelAndClassPart = this.hash.split(".")[0];
    const [level, _] = levelAndClassPart.split(":");
    return parseInt(level);
  }

  getClassIndexFromHash() {
    /* Returns the class index from the hash */
    const levelAndClassPart = this.hash.split(".")[0];
    const [_, classIndex] = levelAndClassPart.split(":");
    return parseInt(classIndex);
  }

  getSkillLevel(skillCode) {
    /* Returns skill level in hash based on given skill code */
    const skillIndexPositionInHash = this.skillCodes.indexOf(skillCode);
    const skillPart = this.hash.split(".")[1];
    const skillLevels = skillPart.split(":");
    return parseInt(skillLevels[skillIndexPositionInHash]);
  }

  setDefaultHash() {
    /* Sets the default hash with level=1, classIndex=0, skillLevels=0 */
    let defaultHash = "1:0.";

    const skillCodesLength = this.skillCodes.length;
    this.skillCodes.forEach((_, index) => {
      if (index+1 == skillCodesLength) {
        // last skill level has no . at the end
        defaultHash += "0";
      } else {
        defaultHash += "0:";
      }
    })

    this.hash = defaultHash;
    location.hash = defaultHash;
  }

  setSkillLevel(baseSkillCode, level) {
    const skillIndexPositionInHash = this.skillCodes.indexOf(baseSkillCode);
    const [levelPart, skillsPart] = this.hash.split(".");
    
    let skillsPartAsList = skillsPart.split(":");
    skillsPartAsList[skillIndexPositionInHash] = level;
    
    let newSkillsPart = skillsPartAsList.join(":");

    let hash = `${levelPart}.${newSkillsPart}`;
    this.hash = hash;
    location.hash = hash;
  }

  setLevel(level) {
    const classIndex = this.getClassIndexFromHash();
    let hash = `${level}:${classIndex}.${this.hash.split(".")[1]}`;

    this.hash = hash;
    location.hash = hash;
  }

  setClassIndex(classIndex) {
    const level = this.getLevelFromHash();
    let hash = `${level}:${classIndex}.${this.hash.split(".")[1]}`;

    this.hash = hash;
    location.hash = hash;
  }
}

export default Hash;
