import { Row, Col } from "react-grid-system";
import React from "react";
import Select from "react-select";

import AuthService from "../AuthService";
import CardList from "../shared/CardList";
import { Link } from "react-router-dom";
import Skill, { getNextCode } from "./Skill";

import "../../styles/react-select-override.css";
import "./Planner.css";
import { hasHash, setDefaultHash, getLevelFromCode, getHashObject, updateHashSkillLevel, updateHashInfoPart, getHash } from "./hash_functions";
import SaveBuildModal from "./SaveBuildModa";
import LoadingScreen from "../layout/LoadingScreen";

export default class Planner extends React.Component {
  constructor(props) {
    super(props);
    this.auth = new AuthService();

    this.state = this._getDefaultState();

    this._levelUpSkill = this._levelUpSkill.bind(this);
    this._levelDownSkill = this._levelDownSkill.bind(this);
    this._onLevelChanged = this._onLevelChanged.bind(this);
    this._onClassChanged = this._onClassChanged.bind(this);
  }

  _getDefaultState() {
    return {
      loading: true,
      data: [],
      error: false,
      errorMessage: "",
      selectedLevel: 1,
      selectedClass: "",
      pointsUsed: 0,
      pointsLeft: 0,
      skills: {},
      saveBuildModalOpen: false,
    }
  }

  _init(props) {
    this.plannerClass = props.match.params.class;
    this.setState(this._getDefaultState());
    this.setState({ selectedClass: this.plannerClass });

    document.title = this.plannerClass[0].toUpperCase() + this.plannerClass.substring(1)
    this._fetchData();

    // Level select options
    const maxLevel = this.plannerClass == "ship" ? 99 : 105;

    this.levelOptions = Array.from(Array(maxLevel).keys()).map(n => {
      // n++ skips 0
      n++;
      return { label: n.toString(), value: n }
    })

    // Class select options
    if (this.plannerClass == "explorer") {
      this.classOptions = [
        { label: "Explorer", value: "explorer" },
        { label: "Sniper", value: "sniper" },
        { label: "Excavator", value: "excavator" },
      ]
    }
    else if (this.plannerClass == "noble") {
      this.classOptions = [
        { label: "Noble", value: "noble" },
        { label: "Court Magican", value: "court magican" },
        { label: "Magic Knight", value: "magic knight" },
      ]
    }
    else if (this.plannerClass == "saint") {
      this.classOptions = [
        { label: "Saint", value: "saint" },
        { label: "Priest", value: "priest" },
        { label: "Shaman", value: "shaman" },
      ]
    }
    else if (this.plannerClass == "mercenary") {
      this.classOptions = [
        { label: "Mercenary", value: "mercenary" },
        { label: "Gladiator", value: "gladiator" },
        { label: "Guardian Swordman", value: "guardian swordman" },
      ]
    }
    else {
      this.classOptions = [
        1, 2, 3, 4, 5
      ];
    }
  }

  _resetSkills() {
    let skills = Object.assign({}, this.state.skills);

    Object.keys(skills).forEach(code => {
      let skill = skills[code];
      skill.level = 0;
      skill.allowed = 0;
    })

    this.setState({ skills }, () => {
      setDefaultHash(this.plannerClass);
      this._updatePoints();
    })

  }

  _getRequiredSkills(data) {
    let requiredSkills = [];
    [1, 2, 3, 4, 5].forEach(n => {
      let rSkill = data[`required_skill_${n}`];
      if (rSkill != "*") {
        requiredSkills.push(rSkill);
      }
    })
    return requiredSkills;
  }

  _getChildSkills(skillCode, childSkills = []) {
    /// Recursive function to get all skills that rely on given skillCode
    const {
      data,
      skills,
    } = this.state;

    Object.keys(skills).forEach(key => {
      const skillData = data[key];
      const requiredSkills = this._getRequiredSkills(skillData);

      if (requiredSkills.includes(skillCode)) {
        if (!childSkills.includes(skillData.skill_code)) {
          childSkills.push(skillData.skill_code);
          return this._getChildSkills(skillData.skill_code, childSkills)
        }
      }
    })
    return childSkills;
  }

  _disableChildSkills(code) {
    let skills = Object.assign({}, this.state.skills);

    this._getChildSkills(code).forEach(skillCode => {
      let skill = skills[skillCode];
      skill.level = 0;
      skill.allowed = 0;

      updateHashSkillLevel(skillCode, 0, this.plannerClass);
    })

    this.setState({ skills }, () => {
      this._updatePoints();
    });
  }

  _updateAllowedSkills() {
    const {
      data,
      selectedLevel,
      selectedClass,
    } = this.state;

    let skills = Object.assign({}, this.state.skills);

    Object.keys(skills).forEach(code => {
      let skillObj = skills[code];
      let skillData = data[code];

      if (!(skillData.required_level <= selectedLevel)) {
        return;
      }

      // any class that is present in classes has to match the
      // required class from the skill. If not, return
      if (this.plannerClass != "ship") {
        let classes = ["no class", "noble", "explorer", "saint", "mercenary"];
        const skillRequiredClass = skillData.class_land.toLowerCase();
        if (!(classes.includes(selectedClass))) {
          classes.push(selectedClass);
        }
        if (!(classes.some(c => skillRequiredClass.includes(c)))) {
          skillObj.allowed = false;
          skillObj.level = 0;
          return;
        }
      }

      // Check if required skills are skilled
      let parentsAreSkilled = true;
      const requiredSkills = this._getRequiredSkills(skillData);
      requiredSkills.forEach(skillCode => {
        if (!(skills[skillCode].level >= 1)) {
          parentsAreSkilled = false;
        }
      })
      if (!parentsAreSkilled) {
        return;
      }

      // Allow skill
      skillObj.allowed = true;
    })

    this.setState({ skills })

  }

  _fetchData() {
    this.auth.fetch("GET", `planner/${this.plannerClass}`)
      .then(res => {
        if (res.error) {
          this.setState({ error: true, errorMessage: err.errorMessage })
        }
        else {
          let data = res.body;
          const hashFound = hasHash();

          if (!hasHash()) {
            setDefaultHash(this.plannerClass);
          }
          else {
            var hashObject = getHashObject();
            this.setState({
              selectedLevel: hashObject.level,
              selectedClass: this.classOptions[hashObject.classIndex].value,
            })
          }

          let skills = {};
          Object.keys(data).forEach(key => {
            let skillCode = data[key].skill_code
            if (!Object.keys(skills).includes(skillCode)) {

              let level = 0;
              let allowed = false;
              if (hashFound) {
                level = getLevelFromCode(hashObject, skillCode, this.plannerClass)
                allowed = level == 0 ? false : true;
              }
              skills[skillCode] = { level, allowed }
            }
          });

          this.setState({ loading: false, data, skills }, () => {
            this._updateAllowedSkills();
            this._updatePoints();
          })
        }
      })
  }

  _levelUpRequirementsFullfilled(code, skillObj, data, selectedLevel, pointsLeft) {
    const skillData = data[code];

    if (skillObj.level == skillData.max_level) {
      return false;
    }

    if (pointsLeft <= 0) {
      return false;
    }

    if (!skillObj.allowed) {
      return false;
    }

    const nextSkillData = data[getNextCode(code, skillObj.level)];
    if (nextSkillData.required_level > selectedLevel) {
      return false;
    }

    return true;
  }

  _levelUpSkill(code, shift) {
    const {
      data,
      selectedLevel,
      pointsLeft,
    } = this.state;

    let skills = Object.assign({}, this.state.skills);
    let skillObj = skills[code];

    // Validate if skill can be skilled
    if (!this._levelUpRequirementsFullfilled(code, skillObj, data, selectedLevel, pointsLeft)) {
      return;
    }

    if (shift) {
      let _pointsLeft = pointsLeft;
      Array.from(Array(15).keys()).forEach(_ => {
        if (this._levelUpRequirementsFullfilled(code, skillObj, data, selectedLevel, _pointsLeft)) {
          skillObj.level++;
          _pointsLeft--;
        }
      })
    }
    else {
      skillObj.level++;
    }

    updateHashSkillLevel(code, skillObj.level, this.plannerClass);

    this.setState({ skills }, () => {
      this._updateAllowedSkills();
      this._updatePoints();
    })
  }

  _levelDownSkill(code, shift) {
    let skills = Object.assign({}, this.state.skills);
    let skillObj = skills[code];

    if (skillObj.level == 0) {
      return;
    }

    if (shift) {
      skillObj.level = 0;
    }
    else {
      skillObj.level--;
    }

    if (skillObj.level == 0) {
      this._disableChildSkills(code);
      updateHashSkillLevel(code, 0, this.plannerClass);
    }
    else {
      this.setState({ skills });
      this._updatePoints();
    }
  }

  _getCurrentClassIndex() {
    const {
      selectedClass
    } = this.state;

    let classIndex = 0;
    this.classOptions.forEach((opt, index) => {
      if (opt.value == selectedClass) {
        classIndex = index;
      }
    })
    return classIndex;
  }

  _onLevelChanged(event) {
    const selectedLevel = event.value;
    const previousLevel = this.state.selectedLevel;

    this.setState({ selectedLevel }, () => {
      this._updatePoints();

      // update hash level
      updateHashInfoPart(selectedLevel, this._getCurrentClassIndex())

      // if level is lower than before,
      // reset skills
      if (selectedLevel < previousLevel) {
        this._resetSkills();
      }

      // if level is lower than 40,
      // reset to base class
      if (selectedLevel < 40) {
        this.setState({ selectedClass: this.plannerClass });
      }

      // level was changed so there could be new skills that are now
      // allowed / not allowed
      this._updateAllowedSkills();
    })
  }

  _onClassChanged(event) {
    const {
      selectedLevel
    } = this.state;

    const selectedClass = event.value;

    if (selectedLevel >= 40) {
      this.setState({ selectedClass }, () => {
        // update hash
        updateHashInfoPart(selectedLevel, this._getCurrentClassIndex())

        // class was changed, so there could be cc skills
        // that are now allowed / not allowed anymore
        this._updateAllowedSkills();
        this._updatePoints();
      })
    }

  }

  _updatePoints() {
    const {
      selectedLevel,
      skills
    } = this.state;

    let maxPoints = 0;
    let pointsUsed = 0;
    let pointsLeft = 0;

    if (selectedLevel <= 100) {
      maxPoints = selectedLevel;
    }
    else if (selectedLevel <= 104) {
      maxPoints = 100;
    }
    else if (selectedLevel == 105) {
      maxPoints = 101;
    }

    Object.keys(skills).forEach(code => {
      pointsUsed += skills[code].level;
    })

    pointsLeft = maxPoints - pointsUsed;

    this.setState({ pointsUsed, pointsLeft })
  }

  componentDidMount() {
    this._init(this.props);
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.match.params.class != this.plannerClass) {
      this._init(nextProps);
    }
  }

  render() {
    const {
      loading,
      data,
      error,
      errorMessage,
      skills,
      selectedLevel,
      selectedClass,
      pointsLeft,
      pointsUsed,
      saveBuildModalOpen,
    } = this.state;

    if (error) {
      throw Error(errorMessage);
    }

    if (loading) {
      return <LoadingScreen />;
    }

    const skilltreeBackground = `/static/img/skilltree_backgrounds/${this.plannerClass}.png`;
    const skillArguments = {
      data,
      skills,
      plannerClass: this.plannerClass,
      selectedLevel,
      levelUpFunction: this._levelUpSkill,
      levelDownFunction: this._levelDownSkill,
    };

    return (
      <>
        <SaveBuildModal
          hash={getHash()}
          selectedLevel={selectedLevel}
          selectedClass={selectedClass}
          plannerClass={this.plannerClass}
          isOpen={saveBuildModalOpen}
          onRequestClose={() => this.setState({saveBuildModalOpen: false})}
        />

        <Row justify="center">
          <Col xl={6}>
            <CardList header={true}>
              <div className="skilltree-header">
                <div className="skilltree-header-inner">
                  <Select
                    value={this.levelOptions.filter(option => option.value == selectedLevel)}
                    options={this.levelOptions}
                    onChange={this._onLevelChanged}
                    className="react-container"
                    classNamePrefix="react-select"
                  />

                  {this.plannerClass != "ship" && (
                    <Select
                      value={this.classOptions.filter(option => option.value == selectedClass)}
                      options={this.classOptions}
                      onChange={this._onClassChanged}
                      className="react-container"
                      classNamePrefix="react-select"
                    />
                  )}
                </div>

                <div className="skilltree-header-inner">
                  <div className="skilltree-header-points-wrapper">
                    <span>Points used: {pointsUsed}</span>
                    <span>Points left: {pointsLeft}</span>
                  </div>

                  <Link className="button-style-1" to={`/planner/${this.plannerClass}/builds`}>Builds</Link>
                  {this.auth.loggedIn() && (
                    <button className="button-style-1" onClick={() => this.setState({saveBuildModalOpen: true})}>Add Build</button>
                  )}
                </div>
              </div>

              <div className="skilltree-wrapper">

                <div className="skilltree">
                  <img src={skilltreeBackground} />

                  {this.plannerClass == "explorer" && (
                    <>
                      <Skill code="ck500000" pos={[34, 54]} {...skillArguments} />
                      <Skill code="ck000700" pos={[93, 50]} {...skillArguments} />
                      <Skill code="ck005200" pos={[264, 50]} {...skillArguments} />
                      <Skill code="ck008700" pos={[324, 50]} {...skillArguments} />
                      <Skill code="ck009000" pos={[93, 111]} {...skillArguments} />
                      <Skill code="ck005800" pos={[164, 111]} {...skillArguments} />
                      <Skill code="ck009100" pos={[224, 111]} {...skillArguments} />
                      <Skill code="ck005300" pos={[324, 111]} {...skillArguments} />
                      <Skill code="ck008500" pos={[460, 111]} {...skillArguments} />
                      <Skill code="ck000800" pos={[34, 173]} {...skillArguments} />
                      <Skill code="ck001000" pos={[164, 174]} {...skillArguments} />
                      <Skill code="ck000900" pos={[259, 174]} {...skillArguments} />
                      <Skill code="ck008400" pos={[356, 174]} {...skillArguments} />
                      <Skill code="ck008800" pos={[403, 174]} {...skillArguments} />
                      <Skill code="ck005900" pos={[92, 238]} {...skillArguments} />
                      <Skill code="ck005400" pos={[143, 238]} {...skillArguments} />
                      <Skill code="ck001100" pos={[194, 238]} {...skillArguments} />
                      <Skill code="ck001200" pos={[296, 238]} {...skillArguments} />
                      <Skill code="ck009200" pos={[224, 298]} {...skillArguments} />
                      <Skill code="ck008000" pos={[324, 298]} {...skillArguments} />
                      <Skill code="ck008300" pos={[403, 298]} {...skillArguments} />
                      <Skill code="ck007900" pos={[460, 298]} {...skillArguments} />
                      <Skill code="ck001500" pos={[34, 362]} {...skillArguments} />
                      <Skill code="ck001300" pos={[143, 362]} {...skillArguments} />
                      <Skill code="ck005700" pos={[194, 362]} {...skillArguments} />
                      <Skill code="ck005500" pos={[296, 362]} {...skillArguments} />
                      <Skill code="ck008100" pos={[403, 362]} {...skillArguments} />
                      <Skill code="ck005600" pos={[224, 425]} {...skillArguments} />
                      <Skill code="ck008600" pos={[403, 425]} {...skillArguments} />
                    </>
                  )}

                  {this.plannerClass == "noble" && (
                    <>
                      <Skill code="ck500000" pos={[36, 53]} {...skillArguments} />
                      <Skill code="cp002300" pos={[36, 117]} {...skillArguments} />
                      <Skill code="cp008700" pos={[36, 289]} {...skillArguments} />
                      <Skill code="cp006800" pos={[36, 422]} {...skillArguments} />
                      <Skill code="cp010200" pos={[98, 57]} {...skillArguments} />
                      <Skill code="cp002500" pos={[98, 289]} {...skillArguments} />
                      <Skill code="cp006700" pos={[98, 354]} {...skillArguments} />
                      <Skill code="cp007000" pos={[98, 422]} {...skillArguments} />
                      <Skill code="cp002400" pos={[166, 57]} {...skillArguments} />
                      <Skill code="cp006100" pos={[187, 175]} {...skillArguments} />
                      <Skill code="cp002900" pos={[152, 230]} {...skillArguments} />
                      <Skill code="cp006300" pos={[167, 289]} {...skillArguments} />
                      <Skill code="cp002800" pos={[187, 354]} {...skillArguments} />
                      <Skill code="cp002700" pos={[157, 422]} {...skillArguments} />
                      <Skill code="cp006000" pos={[200, 117]} {...skillArguments} />
                      <Skill code="cp006400" pos={[254, 230]} {...skillArguments} />
                      <Skill code="cp003000" pos={[218, 422]} {...skillArguments} />
                      <Skill code="cp006200" pos={[291, 57]} {...skillArguments} />
                      <Skill code="cp002600" pos={[291, 117]} {...skillArguments} />
                      <Skill code="cp008800" pos={[254, 289]} {...skillArguments} />
                      <Skill code="cp006500" pos={[282, 422]} {...skillArguments} />
                      <Skill code="cp008300" pos={[359, 57]} {...skillArguments} />
                      <Skill code="cp008500" pos={[349, 230]} {...skillArguments} />
                      <Skill code="cp008900" pos={[349, 289]} {...skillArguments} />
                      <Skill code="cp006600" pos={[349, 354]} {...skillArguments} />
                      <Skill code="cp006900" pos={[339, 422]} {...skillArguments} />
                      <Skill code="cp009100" pos={[399, 354]} {...skillArguments} />
                      <Skill code="cp008400" pos={[399, 422]} {...skillArguments} />
                      <Skill code="cp008200" pos={[457, 176]} {...skillArguments} />
                      <Skill code="cp008600" pos={[457, 422]} {...skillArguments} />
                    </>
                  )}

                  {this.plannerClass == "saint" && (
                    <>
                      <Skill code="cp003500" pos={[51, 55]} {...skillArguments} />
                      <Skill code="cp007700" pos={[216, 55]} {...skillArguments} />
                      <Skill code="cp007600" pos={[280, 55]} {...skillArguments} />
                      <Skill code="cp009600" pos={[442, 55]} {...skillArguments} />
                      <Skill code="cp003100" pos={[51, 129]} {...skillArguments} />
                      <Skill code="cp008000" pos={[116, 129]} {...skillArguments} />
                      <Skill code="cp003200" pos={[181, 129]} {...skillArguments} />
                      <Skill code="cp007100" pos={[245, 129]} {...skillArguments} />
                      <Skill code="cp009300" pos={[309, 129]} {...skillArguments} />
                      <Skill code="cp009200" pos={[375, 129]} {...skillArguments} />
                      <Skill code="cp007800" pos={[442, 129]} {...skillArguments} />
                      <Skill code="cp003800" pos={[116, 200]} {...skillArguments} />
                      <Skill code="cp003400" pos={[181, 200]} {...skillArguments} />
                      <Skill code="cp003600" pos={[245, 200]} {...skillArguments} />
                      <Skill code="cp009400" pos={[343, 200]} {...skillArguments} />
                      <Skill code="cp007200" pos={[95, 278]} {...skillArguments} />
                      <Skill code="cp007900" pos={[161, 278]} {...skillArguments} />
                      <Skill code="cp003300" pos={[245, 278]} {...skillArguments} />
                      <Skill code="cp009500" pos={[343, 278]} {...skillArguments} />
                      <Skill code="cp003700" pos={[162, 349]} {...skillArguments} />
                      <Skill code="cp007300" pos={[216, 349]} {...skillArguments} />
                      <Skill code="cp007400" pos={[284, 349]} {...skillArguments} />
                      <Skill code="cp009800" pos={[343, 349]} {...skillArguments} />
                      <Skill code="cp009700" pos={[392, 349]} {...skillArguments} />
                      <Skill code="cp010100" pos={[442, 349]} {...skillArguments} />
                      <Skill code="ck500000" pos={[51, 420]} {...skillArguments} />
                      <Skill code="cp010300" pos={[116, 420]} {...skillArguments} />
                      <Skill code="cp008100" pos={[267, 420]} {...skillArguments} />
                      <Skill code="cp007500" pos={[321, 420]} {...skillArguments} />
                      <Skill code="cp009900" pos={[392, 420]} {...skillArguments} />
                    </>
                  )}

                  {this.plannerClass == "mercenary" && (
                    <>
                      <Skill code="ck500000" pos={[55, 52]} {...skillArguments} />
                      <Skill code="ck004600" pos={[238, 48]} {...skillArguments} />
                      <Skill code="ck000400" pos={[304, 48]} {...skillArguments} />
                      <Skill code="ck008900" pos={[438, 48]} {...skillArguments} />
                      <Skill code="ck000100" pos={[109, 120]} {...skillArguments} />
                      <Skill code="ck004700" pos={[169, 120]} {...skillArguments} />
                      <Skill code="ck004200" pos={[238, 120]} {...skillArguments} />
                      <Skill code="ck004400" pos={[304, 120]} {...skillArguments} />
                      <Skill code="ck007000" pos={[438, 120]} {...skillArguments} />
                      <Skill code="ck003900" pos={[55, 195]} {...skillArguments} />
                      <Skill code="ck000000" pos={[109, 195]} {...skillArguments} />
                      <Skill code="ck004000" pos={[169, 195]} {...skillArguments} />
                      <Skill code="ck004300" pos={[249, 201]} {...skillArguments} />
                      <Skill code="ck004500" pos={[314, 201]} {...skillArguments} />
                      <Skill code="ck007600" pos={[375, 201]} {...skillArguments} />
                      <Skill code="ck007400" pos={[438, 201]} {...skillArguments} />
                      <Skill code="ck004100" pos={[109, 270]} {...skillArguments} />
                      <Skill code="ck004800" pos={[169, 270]} {...skillArguments} />
                      <Skill code="ck000500" pos={[238, 270]} {...skillArguments} />
                      <Skill code="ck007100" pos={[438, 271]} {...skillArguments} />
                      <Skill code="ck004900" pos={[55, 383]} {...skillArguments} />
                      <Skill code="ck005100" pos={[109, 346]} {...skillArguments} />
                      <Skill code="ck000300" pos={[169, 346]} {...skillArguments} />
                      <Skill code="ck005000" pos={[238, 346]} {...skillArguments} />
                      <Skill code="ck007500" pos={[357, 346]} {...skillArguments} />
                      <Skill code="ck007800" pos={[438, 346]} {...skillArguments} />
                      <Skill code="ck000200" pos={[109, 426]} {...skillArguments} />
                      <Skill code="ck000600" pos={[169, 426]} {...skillArguments} />
                      <Skill code="ck007700" pos={[280, 426]} {...skillArguments} />
                      <Skill code="ck007200" pos={[375, 426]} {...skillArguments} />
                    </>
                  )}

                  {this.plannerClass == "ship" && (
                    <>
                      <Skill code="sksinso00" pos={[49, 48]} {...skillArguments} />
                      <Skill code="skpogye00" pos={[94, 48]} {...skillArguments} />
                      <Skill code="skjojun00" pos={[141, 48]} {...skillArguments} />
                      <Skill code="skwehyu00" pos={[189, 48]} {...skillArguments} />
                      <Skill code="skpokba00" pos={[284, 48]} {...skillArguments} />
                      <Skill code="skchain00" pos={[336, 48]} {...skillArguments} />
                      <Skill code="skadomi00" pos={[443, 48]} {...skillArguments} />
                      <Skill code="skhwaks00" pos={[141, 107]} {...skillArguments} />
                      <Skill code="skstst000" pos={[236, 107]} {...skillArguments} />
                      <Skill code="skgwant00" pos={[284, 107]} {...skillArguments} />
                      <Skill code="skrange00" pos={[390, 107]} {...skillArguments} />
                      <Skill code="skunpro00" pos={[443, 107]} {...skillArguments} />
                      <Skill code="skgyeon00" pos={[49, 168]} {...skillArguments} />
                      <Skill code="skjilju00" pos={[94, 168]} {...skillArguments} />
                      <Skill code="skwinds00" pos={[189, 168]} {...skillArguments} />
                      <Skill code="skpagoe00" pos={[284, 168]} {...skillArguments} />
                      <Skill code="skransh00" pos={[336, 168]} {...skillArguments} />
                      <Skill code="skadest00" pos={[443, 168]} {...skillArguments} />
                      <Skill code="skyeonb00" pos={[49, 232]} {...skillArguments} />
                      <Skill code="skgeunj00" pos={[94, 232]} {...skillArguments} />
                      <Skill code="skangae00" pos={[141, 232]} {...skillArguments} />
                      <Skill code="skhide000" pos={[189, 232]} {...skillArguments} />
                      <Skill code="skdarks00" pos={[236, 232]} {...skillArguments} />
                      <Skill code="skchung00" pos={[284, 232]} {...skillArguments} />
                      <Skill code="skload000" pos={[390, 232]} {...skillArguments} />
                      <Skill code="skflash00" pos={[443, 232]} {...skillArguments} />
                      <Skill code="skavoid00" pos={[94, 297]} {...skillArguments} />
                      <Skill code="skjaesa00" pos={[141, 297]} {...skillArguments} />
                      <Skill code="skhambo00" pos={[236, 297]} {...skillArguments} />
                      <Skill code="sksiles00" pos={[284, 297]} {...skillArguments} />
                      <Skill code="skchiyu00" pos={[336, 297]} {...skillArguments} />
                      <Skill code="skshipr00" pos={[443, 297]} {...skillArguments} />
                      <Skill code="skchund00" pos={[94, 361]} {...skillArguments} />
                      <Skill code="skendur00" pos={[189, 361]} {...skillArguments} />
                      <Skill code="sksick000" pos={[236, 361]} {...skillArguments} />
                      <Skill code="skspecs00" pos={[390, 361]} {...skillArguments} />
                      <Skill code="skturn000" pos={[49, 426]} {...skillArguments} />
                      <Skill code="skyuck000" pos={[94, 426]} {...skillArguments} />
                      <Skill code="skjunja00" pos={[141, 426]} {...skillArguments} />
                      <Skill code="skgyeol00" pos={[189, 426]} {...skillArguments} />
                      <Skill code="skjunso00" pos={[236, 426]} {...skillArguments} />
                      <Skill code="skshotm00" pos={[284, 426]} {...skillArguments} />
                      <Skill code="skdouca00" pos={[336, 426]} {...skillArguments} />
                      <Skill code="sklimit00" pos={[443, 426]} {...skillArguments} />
                    </>
                  )}
                </div>

              </div>

            </CardList>
          </Col>
        </Row>
      </>
    )
  }
}