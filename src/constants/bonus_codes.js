const bonusCodes = {
  "0": "Max HP",
  "1": "Max MP",
  "2": "HP recovery",
  "3": "MP recovery",
  "4": "Physical avoidance rate",
  "5": "Moving speed",
  "6": "Melee max attack",
  "7": "Melee min attack",
  "8": "Range max attack",
  "9": "Range min attack",
  "10": "Magic max attack",
  "11": "Magic min attack",
  "12": "Physical defence",
  "13": "Magic resistance",
  "14": "Melee hitting",
  "15": "Long range hitting",
  "16": "Magic hitting",
  "17": "Melee attack speed",
  "18": "Range attack speed",
  "19": "Magic attack speed",
  "20": "Melee distance",
  "21": "Range distance",
  "22": "Magic distance",
  "23": "Melee critical rate",
  "24": "Range critical rate",
  "25": "Magic critical rate",
  "43": "Total Attack",
  "69": "Recovery skill up",
  "76": "DP Recovery",
  "77": "Max EN",
  "78": "EN Recovery",
  "80": "Defence Power",
  "81": "Cannon proof Power",
  "82": "Explosive Resistance",
  //"95": null, // ship cannons
  //"99": null, // ship cannons
  //"102": null, // special weapons
  //"104": null, // special weapons
  //"110": null, // special weapons
  //"106": null, // ship cannons
  "113": "Land EXP",
  "114": "Sea EXP",
  "117": "Fishing rate",
  "126": "All state",
  "129": "All Attack",
  "131": "Attack speed",
  "154": "Fishing time decrease",
  "155": "Constitution",
  "156": "Strength",
  "157": "Intelligence",
  "158": "Dexterity",
  "159": "Wisdom",
  "160": "Will",
}

function getBonuses(item) {
  var bonuses = [];

  [1, 2, 3, 4, 5].map(n => {
    let bonusCode = item[`bonus_code_${n}`];
    if (bonusCode != 4294967295) {
      let bonusName = bonusCodes[bonusCode];
      let bonusOperator = item[`bonus_operator_${n}`];
      let bonusValue = item[`bonus_${n}`];

      // Florensia has negative values, however, not the operator but the value
      // is negative. Fixed with block below.
      if (bonusValue < 0) {
        bonusOperator = "-";
        bonusValue = Math.abs(bonusValue);
      }

      bonuses.push({
        name: bonusName,
        operator: bonusOperator,
        value: bonusValue
      });
    }
  })

  return bonuses;
}

export default getBonuses;
export {
  bonusCodes
};
