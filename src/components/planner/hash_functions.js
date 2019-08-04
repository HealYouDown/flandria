const skillCodesToIndex = {
  explorer: {
    "ck000700": 0,
    "ck000800": 1,
    "ck000900": 2,
    "ck001000": 3,
    "ck001100": 4,
    "ck001200": 5,
    "ck001300": 6,
    "ck001500": 7,
    "ck005200": 8,
    "ck005300": 9,
    "ck005400": 10,
    "ck005500": 11,
    "ck005600": 12,
    "ck005700": 13,
    "ck005800": 14,
    "ck005900": 15,
    "ck007900": 16,
    "ck008000": 17,
    "ck008100": 18,
    "ck008300": 19,
    "ck008400": 20,
    "ck008500": 21,
    "ck008600": 22,
    "ck008700": 23,
    "ck008800": 24,
    "ck009000": 25,
    "ck009100": 26,
    "ck009200": 27,
    "ck500000": 28
  },
  saint: {
    "ck500000": 0,
    "cp003100": 1,
    "cp003200": 2,
    "cp003300": 3,
    "cp003400": 4,
    "cp003500": 5,
    "cp003600": 6,
    "cp003700": 7,
    "cp003800": 8,
    "cp007100": 9,
    "cp007200": 10,
    "cp007300": 11,
    "cp007400": 12,
    "cp007500": 13,
    "cp007600": 14,
    "cp007700": 15,
    "cp007800": 16,
    "cp007900": 17,
    "cp008000": 18,
    "cp008100": 19,
    "cp009200": 20,
    "cp009300": 21,
    "cp009400": 22,
    "cp009500": 23,
    "cp009600": 24,
    "cp009700": 25,
    "cp009800": 26,
    "cp009900": 27,
    "cp010100": 28,
    "cp010300": 29
  },
  noble: {
    "ck500000": 0,
    "cp002300": 1,
    "cp002400": 2,
    "cp002500": 3,
    "cp002600": 4,
    "cp002700": 5,
    "cp002800": 6,
    "cp002900": 7,
    "cp003000": 8,
    "cp006000": 9,
    "cp006100": 10,
    "cp006200": 11,
    "cp006300": 12,
    "cp006400": 13,
    "cp006500": 14,
    "cp006600": 15,
    "cp006700": 16,
    "cp006800": 17,
    "cp006900": 18,
    "cp007000": 19,
    "cp008200": 20,
    "cp008300": 21,
    "cp008400": 22,
    "cp008500": 23,
    "cp008600": 24,
    "cp008700": 25,
    "cp008800": 26,
    "cp008900": 27,
    "cp009100": 28,
    "cp010200": 29
  },
  mercenary: {
    "ck000000": 0,
    "ck000100": 1,
    "ck000200": 2,
    "ck000300": 3,
    "ck000400": 4,
    "ck000500": 5,
    "ck000600": 6,
    "ck003900": 7,
    "ck004000": 8,
    "ck004100": 9,
    "ck004200": 10,
    "ck004300": 11,
    "ck004400": 12,
    "ck004500": 13,
    "ck004600": 14,
    "ck004700": 15,
    "ck004800": 16,
    "ck004900": 17,
    "ck005000": 18,
    "ck005100": 19,
    "ck007000": 20,
    "ck007100": 21,
    "ck007200": 22,
    "ck007400": 23,
    "ck007500": 24,
    "ck007600": 25,
    "ck007700": 26,
    "ck007800": 27,
    "ck008900": 28,
    "ck500000": 29
  },
  ship: {
    "skadest00": 0,
    "skadomi00": 1,
    "skangae00": 2,
    "skavoid00": 3,
    "skchain00": 4,
    "skchiyu00": 5,
    "skchund00": 6,
    "skchung00": 7,
    "skdarks00": 8,
    "skdouca00": 9,
    "skendur00": 10,
    "skflash00": 11,
    "skgeunj00": 12,
    "skgwant00": 13,
    "skgyeol00": 14,
    "skgyeon00": 15,
    "skhambo00": 16,
    "skhide000": 17,
    "skhwaks00": 18,
    "skjaesa00": 19,
    "skjilju00": 20,
    "skjojun00": 21,
    "skjunja00": 22,
    "skjunso00": 23,
    "sklimit00": 24,
    "skload000": 25,
    "skpagoe00": 26,
    "skpogye00": 27,
    "skpokba00": 28,
    "skrange00": 29,
    "skransh00": 30,
    "skshipr00": 31,
    "skshotm00": 32,
    "sksick000": 33,
    "sksiles00": 34,
    "sksinso00": 35,
    "skspecs00": 36,
    "skstst000": 37,
    "skturn000": 38,
    "skunpro00": 39,
    "skwehyu00": 40,
    "skwinds00": 41,
    "skyeonb00": 42,
    "skyuck000": 43
  },
}

function getHash() {
  return location.hash.replace("#", "");
}

function hasHash() {
  // 5 is a random number, shouldn't be 0 that's all :shrug:
  if (getHash().length > 5) {
    return true;
  }
  return false;
}

function getLevelFromCode(hashObject, code, plannerClass) {
  return hashObject.skills[skillCodesToIndex[plannerClass][code]];
}

function updateHashSkillLevel(code, level, plannerClass) {
  let newHashObject = getHashObject();
  newHashObject.skills[skillCodesToIndex[plannerClass][code]] = level;
  
  updateHash(newHashObject);
}

function updateHashInfoPart(level, classIndex) {
  let newHashObject = getHashObject();
  newHashObject.level = level;
  newHashObject.classIndex = classIndex;

  updateHash(newHashObject);
}

function setDefaultHash(plannerClass) {
  const scti = skillCodesToIndex[plannerClass];
  const sctiLength = Object.keys(scti).length;

  let hash = "";
  hash += "1:0.";

  Array.from(Array(sctiLength).keys()).forEach(num => {
    if (num+1 == sctiLength) {
      hash += "0";
    }
    else {
      hash += "0:";
    }
  })
  location.hash = hash;
}

function getHashObject() {
  // Hash is build up like:
  // 105.1:1:0:0:0:3:4:5:131:3:1:5 ......
  // 105 = level
  // 1 = selected class index
  // everything after the : are the skill levels
  let obj = {};

  // Splits at the first :
  let [infoPart, skillLevelPart] = getHash().split(".")//.split(/:(.+)/)

  // Infos
  obj.level = parseInt(infoPart.split(":")[0]);
  obj.classIndex = parseInt(infoPart.split(":")[1]);

  // Skills
  let skills = [];
  skillLevelPart.split(":").forEach(l => {
    skills.push(parseInt(l));
  })
  obj.skills = skills;

  return obj;
}

function updateHash(hashObject) {
  let hash = `${hashObject.level}:${hashObject.classIndex}.`;
  const skillsLength = Object.keys(hashObject.skills).length;

  Object.values(hashObject.skills).forEach((level, index) => {
    if (index+1 == skillsLength) {
      hash += `${level}`;
    }
    else {
      hash += `${level}:`;
    }
  })

  location.hash = hash;
}

export {
  hasHash, setDefaultHash, getHashObject, getLevelFromCode,
  updateHashSkillLevel, updateHashInfoPart, getHash,
}
