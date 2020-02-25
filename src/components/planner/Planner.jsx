import React, { useState, useEffect } from "react";
import { getPlannerData } from "../fetch";
import TopBarProgress from "react-topbar-progress-indicator";
import { Row, Col } from "react-grid-system";
import Card, { CardHeader, CardBody } from "../common/Card";
import styled from "styled-components";
import Select from "react-select";
import "../../styles/react-select.css";
import classSelectOptions from "./classSelectOptions";
import Hash from "./hash";
import Skill, { getNextCode } from "./Skill";

const SkilltreeHeaderWrapper = styled.div`
  display: flex;
  flex-flow: column;

`;

const SkilltreeHeaderSelectWrapper = styled.div`
  flex-grow: 1;
  display: flex;
  flex-flow: row;

  > div {
    flex-grow: 1;
  }

  > div:not(:first-child) {
    margin-left: 10px;
  }
`

const SkilltreeHeaderLabelsWrapper = styled.div`
  display: flex;
  flex-flow: row;
  justify-content: space-evenly;
  margin-top: 10px;
`

const SkilltreeWrapper = styled.div`
  display: flex;
  flex-flow: row;
  justify-content: center;
  align-items: center;
  height: 100%;

  * {
    user-select: none;
  }
`;

const Skilltree = styled.div`
  width: 525px;
  height: 525px;
  position: relative;
  overflow-y: hidden;
  overflow-x: auto;
  background-attachment: scroll;
`;

class Planner extends React.Component {
  constructor(props) {
    super(props);

    this.init = this.init.bind(this);
    this.onLevelChange = this.onLevelChange.bind(this);
    this.onClassChange = this.onClassChange.bind(this);
    this.levelUpSkill = this.levelUpSkill.bind(this);
    this.levelDownSkill = this.levelDownSkill.bind(this);

    // State
    this.init(props);
    this.state = this.getDefaultState();
  }

  init(props) {
    this.plannerClass = props.match.params.plannerClass;

    // Construct array of level options for select input
    this.levelOptions = [];
    const maxLevel = this.plannerClass == "ship" ? 99 : 105;
    
    new Array(maxLevel+1 - 1).fill().map((d, i) => i + 1).map(num => {
      this.levelOptions.push({label: num.toString(), value: num});
    });

    // Class select options
    // will be empty for ship and not be rendered
    this.classOptions = classSelectOptions[this.plannerClass];

    // fetch data
    getPlannerData(this.plannerClass)
      .then(res => res.json())
      .then(json => {
        // Converts response which consists of arrays
        // to [code] = {data}
        this.skillData = {};
        json.skill_data.forEach(data => {
          this.skillData[data.code] = data;
        })
        // skill codes for this class
        this.skillCodes = json.skill_codes;

        this.hash = new Hash(this.plannerClass, this.skillCodes);
        if (!this.hash.exists()) {
          // add a default hash
          this.hash.setDefaultHash();
        } else {
          // Update state based on hash
          const currentLevel = this.hash.getLevelFromHash();
          const selectedClass = this.plannerClass == "ship" ? "" : this.classOptions[this.hash.getClassIndexFromHash()].value;
          this.setState({currentLevel, selectedClass});
        }

        // add skills object
        let skills = {};
        this.skillCodes.forEach(skillCode => {
          skills[skillCode] = {
            level: this.hash.getSkillLevel(skillCode),
            allowed: false,
          }
        })

        this.setState({skills, loading: false}, () => {
          this.updatePoints();
          this.updateAllowedSkills();
        });
      });
  }

  getDefaultState() {
    return {
      loading: true,

      currentLevel: this.levelOptions[0].value,
      selectedClass: this.plannerClass == "ship" ? "" : this.classOptions[0].value,

      pointsUsed: 0,
      pointsLeft: 1,

      skills: {},
    }
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.match.params.plannerClass != this.plannerClass) {
      this.init(nextProps);
      this.setState(this.getDefaultState());
    }
  }

  onLevelChange(option) {
    let value = option.value;
    if (value < this.state.currentLevel) {
      // reset because level was changed to a lower value
      let skills = Object.assign({}, this.state.skills);
      Object.keys(skills).forEach(baseSkillCode => {
        let skill = skills[baseSkillCode];
        skill.allowed = false;
        skill.level = 0;
        
        this.hash.setSkillLevel(baseSkillCode, 0);
        this.setState({skills});
      })

      // if level is now smaller than 40, reset class
      if (value < 40) {
        if (!this.plannerClass == "ship") {
          this.setState({selectedClass: this.classOptions[0].value}, () => {
            // reset class index in hash
            this.hash.setClassIndex(0);
          })
        }
      }
    }

    this.setState({currentLevel: value}, () => {
      // Update points
      this.updatePoints();
      // Update hash
      this.hash.setLevel(this.state.currentLevel);
      // Update allowed skills
      this.updateAllowedSkills();
    })
  }

  onClassChange(option) {
    let value = option.value;
    if (!["noble", "explorer", "mercenary", "saint"].includes(value) && this.state.currentLevel < 40) {
      return;
    }
    this.setState({selectedClass: value}, () => {
      // Update hash
      this.hash.setClassIndex(this.classOptions.indexOf(option));
      // update allowed skills
      this.updateAllowedSkills();
      // update points
      this.updatePoints();
    });
  }

  levelUpSkill(baseSkillCode, isShifted) {
    let skills = Object.assign({}, this.state.skills);
    let skill = skills[baseSkillCode];

    if (!this.skillLevelUpRequirementsFullfilled(baseSkillCode, skill, this.state.pointsLeft)) {
      return;
    }

    if (isShifted) {
      let pointsLeft = this.state.pointsLeft;
      Array.from(Array(15).keys()).forEach(_ => {
        if (this.skillLevelUpRequirementsFullfilled(baseSkillCode, skill, pointsLeft)) {
          skill.level++;
          pointsLeft--;
        }
      })
    } else {
      skill.level++;
    }

    this.hash.setSkillLevel(baseSkillCode, skill.level);

    this.setState({skills}, () => {
      this.updateAllowedSkills();
      this.updatePoints();
    })
  }

  levelDownSkill(baseSkillCode, isShifted) {
    let skills = Object.assign({}, this.state.skills);
    let skill = skills[baseSkillCode];

    if (skill.level == 0) {
      return;
    }

    if (isShifted) {
      skill.level = 0;
    } else {
      skill.level--;
    }

    if (skill.level == 0) {
      // disable all child skills
      this.getChildSkillCodes(baseSkillCode, []).forEach(childSkillCode => {
        let childSkill = skills[childSkillCode];
        childSkill.level = 0;
        childSkill.allowed = false;

        this.hash.setSkillLevel(childSkillCode, 0);
      });

    }

    this.hash.setSkillLevel(baseSkillCode, skill.level);

    this.setState({skills}, () => {
      this.updatePoints();
    })
  }

  skillLevelUpRequirementsFullfilled(baseSkillCode, skill, pointsLeft) {
    const maxLevel = this.skillData[baseSkillCode].max_level;

    if (skill.level == maxLevel) {
      return false;
    }

    if (pointsLeft <= 0) {
      return false;
    }

    if (!skill.allowed) {
      return false;
    }

    const nextData = this.skillData[getNextCode(baseSkillCode, skill.level)];
    if (nextData.required_level > this.state.currentLevel) {
      return false;
    }

    return true;
  }

  updatePoints() {
    let maxPoints = 0;
    let pointsUsed = 0;
    let pointsLeft = 0;

    if (this.state.currentLevel <= 100) {
      maxPoints = this.state.currentLevel;
    } else if (this.state.currentLevel <= 104) {
      maxPoints = 100;
    } else if (this.state.currentLevel == 105) {
      maxPoints = 101;
    }

    // Calculate current used points
    Object.keys(this.state.skills).forEach(baseSkillCode => {
      pointsUsed += this.state.skills[baseSkillCode].level;
    })

    pointsLeft = maxPoints - pointsUsed;

    this.setState({pointsLeft, pointsUsed});
  }

  getChildSkillCodes(skillCode, codes) {
    Object.keys(this.state.skills).forEach(baseSkillCode => {
      const data = this.skillData[baseSkillCode];

      if (data.required_skills.includes(skillCode)) {
        if (!codes.includes(baseSkillCode)) {
          codes.push(baseSkillCode);
          return this.getChildSkillCodes(baseSkillCode, codes);
        }
      }
    });

    return codes;
  }  

  updateAllowedSkills() {
    let skills = Object.assign({}, this.state.skills);

    Object.keys(skills).forEach(baseSkillCode => {
      let skill = skills[baseSkillCode];
      let data = this.skillData[baseSkillCode];

      if (data.required_level > this.state.currentLevel) {
        return;
      }

      if (this.plannerClass != "ship") {
        let classes = ["no class", "noble", "explorer", "saint", "mercenary"];
        // adds select (cc) class to list to check against
        if (!classes.includes(this.state.selectedClass)) {
          classes.push(this.state.selectedClass);
        }

        const requiredSkillClasses = data.class_land.toLowerCase();
        if (!classes.some(classString => requiredSkillClasses.includes(classString))) {
          // disable (cc) skills
          skill.allowed = false;
          skill.level = 0;
          return;
        }
      }

      // check if parent skill is skilled
      // if child does not rely on any other skill, it
      // will pass this check
      let parentsAreSkilled = true;
      data.required_skills.forEach(requiredSkillBaseCode => {
        if (!skills[requiredSkillBaseCode].level > 0) {
          parentsAreSkilled = false;
        }
      })
      if (!parentsAreSkilled) {
        return;
      }

      skill.allowed = true;

      this.setState({skills});
    })

  }

  render() {
    if (this.state.loading) {
      return <TopBarProgress />;
    }

    const skillArguments = {
      plannerClass: this.plannerClass,
      skills: this.state.skills,
      skillData: this.skillData,
      levelDown: this.levelDownSkill,
      levelUp: this.levelUpSkill,
      currentLevel: this.state.currentLevel,
    }

    let skills;
    if (this.plannerClass == "explorer") {
      skills = [
        <Skill baseSkillCode="ck500000" pos={[34, 54]} {...skillArguments} />,
        <Skill baseSkillCode="ck000700" pos={[93, 50]} {...skillArguments} />,
        <Skill baseSkillCode="ck005200" pos={[264, 50]} {...skillArguments} />,
        <Skill baseSkillCode="ck008700" pos={[324, 50]} {...skillArguments} />,
        <Skill baseSkillCode="ck009000" pos={[93, 111]} {...skillArguments} />,
        <Skill baseSkillCode="ck005800" pos={[164, 111]} {...skillArguments} />,
        <Skill baseSkillCode="ck009100" pos={[224, 111]} {...skillArguments} />,
        <Skill baseSkillCode="ck005300" pos={[324, 111]} {...skillArguments} />,
        <Skill baseSkillCode="ck008500" pos={[460, 111]} {...skillArguments} />,
        <Skill baseSkillCode="ck000800" pos={[34, 173]} {...skillArguments} />,
        <Skill baseSkillCode="ck001000" pos={[164, 174]} {...skillArguments} />,
        <Skill baseSkillCode="ck000900" pos={[259, 174]} {...skillArguments} />,
        <Skill baseSkillCode="ck008400" pos={[356, 174]} {...skillArguments} />,
        <Skill baseSkillCode="ck008800" pos={[403, 174]} {...skillArguments} />,
        <Skill baseSkillCode="ck005900" pos={[92, 238]} {...skillArguments} />,
        <Skill baseSkillCode="ck005400" pos={[143, 238]} {...skillArguments} />,
        <Skill baseSkillCode="ck001100" pos={[194, 238]} {...skillArguments} />,
        <Skill baseSkillCode="ck001200" pos={[296, 238]} {...skillArguments} />,
        <Skill baseSkillCode="ck009200" pos={[224, 298]} {...skillArguments} />,
        <Skill baseSkillCode="ck008000" pos={[324, 298]} {...skillArguments} />,
        <Skill baseSkillCode="ck008300" pos={[403, 298]} {...skillArguments} />,
        <Skill baseSkillCode="ck007900" pos={[460, 298]} {...skillArguments} />,
        <Skill baseSkillCode="ck001500" pos={[34, 362]} {...skillArguments} />,
        <Skill baseSkillCode="ck001300" pos={[143, 362]} {...skillArguments} />,
        <Skill baseSkillCode="ck005700" pos={[194, 362]} {...skillArguments} />,
        <Skill baseSkillCode="ck005500" pos={[296, 362]} {...skillArguments} />,
        <Skill baseSkillCode="ck008100" pos={[403, 362]} {...skillArguments} />,
        <Skill baseSkillCode="ck005600" pos={[224, 425]} {...skillArguments} />,
        <Skill baseSkillCode="ck008600" pos={[403, 425]} {...skillArguments} />,
      ]
    } else if (this.plannerClass == "noble") {
      skills = [
        <Skill baseSkillCode="ck500000" pos={[36, 53]} {...skillArguments} />,
        <Skill baseSkillCode="cp002300" pos={[36, 117]} {...skillArguments} />,
        <Skill baseSkillCode="cp008700" pos={[36, 289]} {...skillArguments} />,
        <Skill baseSkillCode="cp006800" pos={[36, 422]} {...skillArguments} />,
        <Skill baseSkillCode="cp010200" pos={[98, 57]} {...skillArguments} />,
        <Skill baseSkillCode="cp002500" pos={[98, 289]} {...skillArguments} />,
        <Skill baseSkillCode="cp006700" pos={[98, 354]} {...skillArguments} />,
        <Skill baseSkillCode="cp007000" pos={[98, 422]} {...skillArguments} />,
        <Skill baseSkillCode="cp002400" pos={[166, 57]} {...skillArguments} />,
        <Skill baseSkillCode="cp006100" pos={[187, 175]} {...skillArguments} />,
        <Skill baseSkillCode="cp002900" pos={[152, 230]} {...skillArguments} />,
        <Skill baseSkillCode="cp006300" pos={[167, 289]} {...skillArguments} />,
        <Skill baseSkillCode="cp002800" pos={[187, 354]} {...skillArguments} />,
        <Skill baseSkillCode="cp002700" pos={[157, 422]} {...skillArguments} />,
        <Skill baseSkillCode="cp006000" pos={[200, 117]} {...skillArguments} />,
        <Skill baseSkillCode="cp006400" pos={[254, 230]} {...skillArguments} />,
        <Skill baseSkillCode="cp003000" pos={[218, 422]} {...skillArguments} />,
        <Skill baseSkillCode="cp006200" pos={[291, 57]} {...skillArguments} />,
        <Skill baseSkillCode="cp002600" pos={[291, 117]} {...skillArguments} />,
        <Skill baseSkillCode="cp008800" pos={[254, 289]} {...skillArguments} />,
        <Skill baseSkillCode="cp006500" pos={[282, 422]} {...skillArguments} />,
        <Skill baseSkillCode="cp008300" pos={[359, 57]} {...skillArguments} />,
        <Skill baseSkillCode="cp008500" pos={[349, 230]} {...skillArguments} />,
        <Skill baseSkillCode="cp008900" pos={[349, 289]} {...skillArguments} />,
        <Skill baseSkillCode="cp006600" pos={[349, 354]} {...skillArguments} />,
        <Skill baseSkillCode="cp006900" pos={[339, 422]} {...skillArguments} />,
        <Skill baseSkillCode="cp009100" pos={[399, 354]} {...skillArguments} />,
        <Skill baseSkillCode="cp008400" pos={[399, 422]} {...skillArguments} />,
        <Skill baseSkillCode="cp008200" pos={[457, 176]} {...skillArguments} />,
        <Skill baseSkillCode="cp008600" pos={[457, 422]} {...skillArguments} />,
      ]
    } else if (this.plannerClass == "saint") {
      skills = [
        <Skill baseSkillCode="cp003500" pos={[51, 55]} {...skillArguments} />,
        <Skill baseSkillCode="cp007700" pos={[216, 55]} {...skillArguments} />,
        <Skill baseSkillCode="cp007600" pos={[280, 55]} {...skillArguments} />,
        <Skill baseSkillCode="cp009600" pos={[442, 55]} {...skillArguments} />,
        <Skill baseSkillCode="cp003100" pos={[51, 129]} {...skillArguments} />,
        <Skill baseSkillCode="cp008000" pos={[116, 129]} {...skillArguments} />,
        <Skill baseSkillCode="cp003200" pos={[181, 129]} {...skillArguments} />,
        <Skill baseSkillCode="cp007100" pos={[245, 129]} {...skillArguments} />,
        <Skill baseSkillCode="cp009300" pos={[309, 129]} {...skillArguments} />,
        <Skill baseSkillCode="cp009200" pos={[375, 129]} {...skillArguments} />,
        <Skill baseSkillCode="cp007800" pos={[442, 129]} {...skillArguments} />,
        <Skill baseSkillCode="cp003800" pos={[116, 200]} {...skillArguments} />,
        <Skill baseSkillCode="cp003400" pos={[181, 200]} {...skillArguments} />,
        <Skill baseSkillCode="cp003600" pos={[245, 200]} {...skillArguments} />,
        <Skill baseSkillCode="cp009400" pos={[343, 200]} {...skillArguments} />,
        <Skill baseSkillCode="cp007200" pos={[95, 278]} {...skillArguments} />,
        <Skill baseSkillCode="cp007900" pos={[161, 278]} {...skillArguments} />,
        <Skill baseSkillCode="cp003300" pos={[245, 278]} {...skillArguments} />,
        <Skill baseSkillCode="cp009500" pos={[343, 278]} {...skillArguments} />,
        <Skill baseSkillCode="cp003700" pos={[162, 349]} {...skillArguments} />,
        <Skill baseSkillCode="cp007300" pos={[216, 349]} {...skillArguments} />,
        <Skill baseSkillCode="cp007400" pos={[284, 349]} {...skillArguments} />,
        <Skill baseSkillCode="cp009800" pos={[343, 349]} {...skillArguments} />,
        <Skill baseSkillCode="cp009700" pos={[392, 349]} {...skillArguments} />,
        <Skill baseSkillCode="cp010100" pos={[442, 349]} {...skillArguments} />,
        <Skill baseSkillCode="ck500000" pos={[51, 420]} {...skillArguments} />,
        <Skill baseSkillCode="cp010300" pos={[116, 420]} {...skillArguments} />,
        <Skill baseSkillCode="cp008100" pos={[267, 420]} {...skillArguments} />,
        <Skill baseSkillCode="cp007500" pos={[321, 420]} {...skillArguments} />,
        <Skill baseSkillCode="cp009900" pos={[392, 420]} {...skillArguments} />,
      ]
    } else if (this.plannerClass == "mercenary") {
      skills = [
        <Skill baseSkillCode="ck500000" pos={[55, 52]} {...skillArguments} />,
        <Skill baseSkillCode="ck004600" pos={[238, 48]} {...skillArguments} />,
        <Skill baseSkillCode="ck000400" pos={[304, 48]} {...skillArguments} />,
        <Skill baseSkillCode="ck008900" pos={[438, 48]} {...skillArguments} />,
        <Skill baseSkillCode="ck000100" pos={[109, 120]} {...skillArguments} />,
        <Skill baseSkillCode="ck004700" pos={[169, 120]} {...skillArguments} />,
        <Skill baseSkillCode="ck004200" pos={[238, 120]} {...skillArguments} />,
        <Skill baseSkillCode="ck004400" pos={[304, 120]} {...skillArguments} />,
        <Skill baseSkillCode="ck007000" pos={[438, 120]} {...skillArguments} />,
        <Skill baseSkillCode="ck003900" pos={[55, 195]} {...skillArguments} />,
        <Skill baseSkillCode="ck000000" pos={[109, 195]} {...skillArguments} />,
        <Skill baseSkillCode="ck004000" pos={[169, 195]} {...skillArguments} />,
        <Skill baseSkillCode="ck004300" pos={[249, 201]} {...skillArguments} />,
        <Skill baseSkillCode="ck004500" pos={[314, 201]} {...skillArguments} />,
        <Skill baseSkillCode="ck007600" pos={[375, 201]} {...skillArguments} />,
        <Skill baseSkillCode="ck007400" pos={[438, 201]} {...skillArguments} />,
        <Skill baseSkillCode="ck004100" pos={[109, 270]} {...skillArguments} />,
        <Skill baseSkillCode="ck004800" pos={[169, 270]} {...skillArguments} />,
        <Skill baseSkillCode="ck000500" pos={[238, 270]} {...skillArguments} />,
        <Skill baseSkillCode="ck007100" pos={[438, 271]} {...skillArguments} />,
        <Skill baseSkillCode="ck004900" pos={[55, 383]} {...skillArguments} />,
        <Skill baseSkillCode="ck005100" pos={[109, 346]} {...skillArguments} />,
        <Skill baseSkillCode="ck000300" pos={[169, 346]} {...skillArguments} />,
        <Skill baseSkillCode="ck005000" pos={[238, 346]} {...skillArguments} />,
        <Skill baseSkillCode="ck007500" pos={[357, 346]} {...skillArguments} />,
        <Skill baseSkillCode="ck007800" pos={[438, 346]} {...skillArguments} />,
        <Skill baseSkillCode="ck000200" pos={[109, 426]} {...skillArguments} />,
        <Skill baseSkillCode="ck000600" pos={[169, 426]} {...skillArguments} />,
        <Skill baseSkillCode="ck007700" pos={[280, 426]} {...skillArguments} />,
        <Skill baseSkillCode="ck007200" pos={[375, 426]} {...skillArguments} />,
      ]
    } else if (this.plannerClass == "ship") {
      skills = [
        <Skill baseSkillCode="sksinso00" pos={[49, 48]} {...skillArguments} />,
        <Skill baseSkillCode="skpogye00" pos={[94, 48]} {...skillArguments} />,
        <Skill baseSkillCode="skjojun00" pos={[141, 48]} {...skillArguments} />,
        <Skill baseSkillCode="skwehyu00" pos={[189, 48]} {...skillArguments} />,
        <Skill baseSkillCode="skpokba00" pos={[284, 48]} {...skillArguments} />,
        <Skill baseSkillCode="skchain00" pos={[336, 48]} {...skillArguments} />,
        <Skill baseSkillCode="skadomi00" pos={[443, 48]} {...skillArguments} />,
        <Skill baseSkillCode="skhwaks00" pos={[141, 107]} {...skillArguments} />,
        <Skill baseSkillCode="skstst000" pos={[236, 107]} {...skillArguments} />,
        <Skill baseSkillCode="skgwant00" pos={[284, 107]} {...skillArguments} />,
        <Skill baseSkillCode="skrange00" pos={[390, 107]} {...skillArguments} />,
        <Skill baseSkillCode="skunpro00" pos={[443, 107]} {...skillArguments} />,
        <Skill baseSkillCode="skgyeon00" pos={[49, 168]} {...skillArguments} />,
        <Skill baseSkillCode="skjilju00" pos={[94, 168]} {...skillArguments} />,
        <Skill baseSkillCode="skwinds00" pos={[189, 168]} {...skillArguments} />,
        <Skill baseSkillCode="skpagoe00" pos={[284, 168]} {...skillArguments} />,
        <Skill baseSkillCode="skransh00" pos={[336, 168]} {...skillArguments} />,
        <Skill baseSkillCode="skadest00" pos={[443, 168]} {...skillArguments} />,
        <Skill baseSkillCode="skyeonb00" pos={[49, 232]} {...skillArguments} />,
        <Skill baseSkillCode="skgeunj00" pos={[94, 232]} {...skillArguments} />,
        <Skill baseSkillCode="skangae00" pos={[141, 232]} {...skillArguments} />,
        <Skill baseSkillCode="skhide000" pos={[189, 232]} {...skillArguments} />,
        <Skill baseSkillCode="skdarks00" pos={[236, 232]} {...skillArguments} />,
        <Skill baseSkillCode="skchung00" pos={[284, 232]} {...skillArguments} />,
        <Skill baseSkillCode="skload000" pos={[390, 232]} {...skillArguments} />,
        <Skill baseSkillCode="skflash00" pos={[443, 232]} {...skillArguments} />,
        <Skill baseSkillCode="skavoid00" pos={[94, 297]} {...skillArguments} />,
        <Skill baseSkillCode="skjaesa00" pos={[141, 297]} {...skillArguments} />,
        <Skill baseSkillCode="skhambo00" pos={[236, 297]} {...skillArguments} />,
        <Skill baseSkillCode="sksiles00" pos={[284, 297]} {...skillArguments} />,
        <Skill baseSkillCode="skchiyu00" pos={[336, 297]} {...skillArguments} />,
        <Skill baseSkillCode="skshipr00" pos={[443, 297]} {...skillArguments} />,
        <Skill baseSkillCode="skchund00" pos={[94, 361]} {...skillArguments} />,
        <Skill baseSkillCode="skendur00" pos={[189, 361]} {...skillArguments} />,
        <Skill baseSkillCode="sksick000" pos={[236, 361]} {...skillArguments} />,
        <Skill baseSkillCode="skspecs00" pos={[390, 361]} {...skillArguments} />,
        <Skill baseSkillCode="skturn000" pos={[49, 426]} {...skillArguments} />,
        <Skill baseSkillCode="skyuck000" pos={[94, 426]} {...skillArguments} />,
        <Skill baseSkillCode="skjunja00" pos={[141, 426]} {...skillArguments} />,
        <Skill baseSkillCode="skgyeol00" pos={[189, 426]} {...skillArguments} />,
        <Skill baseSkillCode="skjunso00" pos={[236, 426]} {...skillArguments} />,
        <Skill baseSkillCode="skshotm00" pos={[284, 426]} {...skillArguments} />,
        <Skill baseSkillCode="skdouca00" pos={[336, 426]} {...skillArguments} />,
        <Skill baseSkillCode="sklimit00" pos={[443, 426]} {...skillArguments} />,
      ]
    }

    return (
      <Row justify="center">
        <Col xl={6}>

          <Card>
            <CardHeader>
              <SkilltreeHeaderWrapper>
                <SkilltreeHeaderSelectWrapper>
                  <Select
                    isSearchable={true}
                    options={this.levelOptions}
                    value={this.levelOptions.filter(opt => opt.value == this.state.currentLevel)}
                    className="react-container"
                    classNamePrefix="react-select"
                    onChange={this.onLevelChange}
                  />
                  {this.plannerClass != "ship" && (
                    <Select
                      isSearchable={true}
                      options={this.classOptions}
                      value={this.classOptions.filter(opt => opt.value == this.state.selectedClass)}
                      className="react-container"
                      classNamePrefix="react-select"
                      onChange={this.onClassChange}
                    />
                  )}
                </SkilltreeHeaderSelectWrapper>
                <SkilltreeHeaderLabelsWrapper>
                  <span>Points used: {this.state.pointsUsed}</span>
                  <span>Points left: {this.state.pointsLeft}</span>
                </SkilltreeHeaderLabelsWrapper>
              </SkilltreeHeaderWrapper>
            </CardHeader>

            <CardBody>
              <SkilltreeWrapper>
                <Skilltree>
                  <img src={`/static/assets/skilltree_backgrounds/${this.plannerClass}.png`} />
                  {skills}
                </Skilltree>
              </SkilltreeWrapper>
            </CardBody>
          </Card>

        </Col>
      </Row>
    )
  }
}

export default Planner;