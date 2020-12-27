const SKILL_LOCATIONS = {
  explorer: {
    ck500000: [18, 14],
    ck000700: [15, 73],
    ck005200: [15, 246],
    ck008700: [15, 306],
    ck009000: [76, 75],
    ck005800: [76, 146],
    ck009100: [76, 206],
    ck005300: [76, 306],
    ck008500: [76, 442],
    ck000800: [138, 16],
    ck001000: [139, 146],
    ck000900: [139, 241],
    ck008400: [139, 338],
    ck008800: [139, 385],
    ck005900: [203, 74],
    ck005400: [203, 125],
    ck001100: [203, 176],
    ck001200: [203, 278],
    ck009200: [263, 206],
    ck008000: [263, 306],
    ck008300: [263, 385],
    ck007900: [263, 442],
    ck001500: [327, 16],
    ck001300: [327, 125],
    ck005700: [327, 176],
    ck005500: [327, 278],
    ck008100: [327, 385],
    ck005600: [390, 206],
    ck008600: [390, 385],
  },
  noble: {
    ck500000: [13, 14],
    cp002300: [77, 14],
    cp008700: [249, 14],
    cp006800: [382, 14],
    cp010200: [17, 76],
    cp002500: [249, 76],
    cp006700: [314, 76],
    cp007000: [382, 76],
    cp002400: [17, 144],
    cp006100: [135, 165],
    cp002900: [190, 130],
    cp006300: [249, 145],
    cp002800: [314, 165],
    cp002700: [382, 135],
    cp006000: [77, 178],
    cp006400: [190, 232],
    cp003000: [382, 196],
    cp006200: [17, 269],
    cp002600: [77, 269],
    cp008800: [249, 232],
    cp006500: [382, 260],
    cp008300: [17, 337],
    cp008500: [190, 327],
    cp008900: [249, 327],
    cp006600: [314, 327],
    cp006900: [382, 317],
    cp009100: [314, 377],
    cp008400: [382, 377],
    cp008200: [136, 435],
    cp008600: [382, 435],
  },
  saint: {
    cp003500: [18, 15],
    cp007700: [18, 180],
    cp007600: [18, 244],
    cp009600: [18, 406],
    cp003100: [92, 15],
    cp008000: [92, 80],
    cp003200: [92, 145],
    cp007100: [92, 209],
    cp009300: [92, 273],
    cp009200: [92, 339],
    cp007800: [92, 406],
    cp003800: [163, 80],
    cp003400: [163, 145],
    cp003600: [163, 209],
    cp009400: [163, 307],
    cp007200: [241, 59],
    cp007900: [241, 125],
    cp003300: [241, 209],
    cp009500: [241, 307],
    cp003700: [312, 126],
    cp007300: [312, 180],
    cp007400: [312, 248],
    cp009800: [312, 307],
    cp009700: [312, 356],
    cp010100: [312, 406],
    ck500000: [383, 15],
    cp010300: [383, 80],
    cp008100: [383, 231],
    cp007500: [383, 285],
    cp009900: [383, 356],
  },
  mercenary: {
    ck500000: [13, 13],
    ck004600: [9, 196],
    ck000400: [9, 262],
    ck008900: [9, 396],
    ck000100: [81, 67],
    ck004700: [81, 127],
    ck004200: [81, 196],
    ck004400: [81, 262],
    ck007000: [81, 396],
    ck003900: [156, 13],
    ck000000: [156, 67],
    ck004000: [156, 127],
    ck004300: [162, 207],
    ck004500: [162, 272],
    ck007600: [162, 334],
    ck007400: [162, 396],
    ck004100: [231, 67],
    ck004800: [231, 127],
    ck000500: [231, 196],
    ck007100: [232, 396],
    ck004900: [344, 13],
    ck005100: [307, 67],
    ck000300: [307, 126],
    ck005000: [307, 196],
    ck007500: [307, 315],
    ck007800: [307, 396],
    ck000200: [387, 67],
    ck000600: [387, 127],
    ck007700: [387, 238],
    ck007200: [387, 333],
  },
  ship: {
    sksinso00: [11, 16],
    skpogye00: [11, 61],
    skjojun00: [11, 108],
    skwehyu00: [11, 156],
    skpokba00: [11, 251],
    skchain00: [11, 303],
    skadomi00: [11, 410],
    skhwaks00: [70, 108],
    skstst000: [71, 204],
    skgwant00: [70, 251],
    skrange00: [70, 357],
    skunpro00: [70, 410],
    skgyeon00: [131, 16],
    skjilju00: [131, 61],
    skwinds00: [131, 156],
    skpagoe00: [131, 251],
    skransh00: [131, 303],
    skadest00: [131, 410],
    skyeonb00: [195, 16],
    skgeunj00: [195, 61],
    skangae00: [195, 108],
    skhide000: [195, 156],
    skdarks00: [195, 203],
    skchung00: [195, 251],
    skload000: [195, 357],
    skflash00: [195, 410],
    skavoid00: [260, 61],
    skjaesa00: [260, 108],
    skhambo00: [260, 203],
    sksiles00: [260, 251],
    skchiyu00: [260, 303],
    skshipr00: [260, 410],
    skchund00: [324, 61],
    skendur00: [324, 156],
    sksick000: [324, 203],
    skspecs00: [324, 357],
    skturn000: [389, 16],
    skyuck000: [389, 61],
    skjunja00: [389, 108],
    skgyeol00: [389, 156],
    skjunso00: [389, 203],
    skshotm00: [389, 251],
    skdouca00: [389, 303],
    sklimit00: [389, 410],
  },
};

class SkillObject {
  constructor(classname, skillCode, skillLevels) {
    // Classname
    this.classname = classname;

    // The base skill code, 00 at the end
    this.skillCode = skillCode;
    // Array with all skill levels (0-15) ordered
    // by skill level.
    this.skillLevels = skillLevels;

    // Contains basic information about icon, class
    // needed etc.
    this.baseSkill = skillLevels[0];

    // Stored information about the skill state in here
    this.skillLevel = 0;
    this.allowed = false;
  }

  getPosition() {
    const position = SKILL_LOCATIONS[this.classname][this.skillCode];
    return {
      left: position[0],
      top: position[1],
    };
  }

  reset() {
    this.skillLevel = 0;
    this.allowed = false;
  }

  getSkillForCurrentLevel() {
    return this.skillLevels[this.skillLevel];
  }

  getSkillForNextLevel() {
    return this.skillLevels[this.skillLevel + 1];
  }

  getRequiredSkills() {
    // Required skills are only available on the base skill object
    return this.baseSkill.required_skills;
  }

  levelUpRequirementsFullfilled(selectedLevel, pointsLeft) {
    if (!this.allowed) {
      return false;
    }

    if (this.skillLevel === this.baseSkill.max_level) {
      return false;
    }

    if (pointsLeft <= 0) {
      return false;
    }

    const nextRequiredLevel = (
      (this.classname === 'ship')
        ? this.getSkillForNextLevel().required_level_sea
        : this.getSkillForNextLevel().required_level_land
    );
    if (nextRequiredLevel > selectedLevel) {
      return false;
    }

    return true;
  }
}

export default SkillObject;
