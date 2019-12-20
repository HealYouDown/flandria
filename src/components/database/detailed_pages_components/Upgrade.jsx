import React from "react";

import CardList, { LabelValueListItem } from "../../shared/CardList";

import "./Upgrade.css";

const weaponTables = ["cariad", "rapier", "dagger", "one_handed_sword", "two_handed_sword", "rifle", "duals"];

export default class Upgrade extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      upgradeLevel: 0,
    }
  }

  render() {
    const {
      table,
      data
    } = this.props;

    const upgradeData = data.upgrade_data;

    if (upgradeData.length != 16)
      return null;

    if (weaponTables.includes(table)) {
      this.phMin = data.physical_attack_min;
      this.phMax = data.physical_attack_max;
      this.mgMin = data.magical_attack_min;
      this.mgMax = data.magical_attack_max;
      this.attackSpeed = data.attack_speed;
      this.range = data.attack_range;

      var stats = (
        <>
          {["rapier", "dagger", "one_handed_sword", "two_handed_sword", "rifle", "duals"].includes(table)
            ? <LabelValueListItem
                label="Physical Damage" 
                value={
                  `
                  ${Math.floor(this.phMin + upgradeData[this.state.upgradeLevel].value_0)} 
                  ~
                  ${Math.floor(this.phMax + upgradeData[this.state.upgradeLevel].value_0)}
                  `
                }
                valueClassName={`upgrade-${this.state.upgradeLevel}`}
              />
            : <LabelValueListItem 
                label="Physical Damage" 
                value={`${this.phMin} ~ ${this.phMax}`}
              />
          }

          {["cariad", "rapier", "dagger"].includes(table)
            ? ["rapier", "dagger"].includes(table)
              ? <LabelValueListItem
                  label="Magical Damage" 
                  value={
                    `
                    ${Math.floor(this.mgMin + upgradeData[this.state.upgradeLevel].value_2)} 
                    ~
                    ${Math.floor(this.mgMax + upgradeData[this.state.upgradeLevel].value_2)}
                    `
                  }
                  valueClassName={`upgrade-${this.state.upgradeLevel}`}
                />
              : <LabelValueListItem
                  label="Magical Damage" 
                  value={
                    `
                    ${Math.floor(this.mgMin + upgradeData[this.state.upgradeLevel].value_1)} 
                    ~
                    ${Math.floor(this.mgMax + upgradeData[this.state.upgradeLevel].value_1)}
                    `
                  }
                  valueClassName={`upgrade-${this.state.upgradeLevel}`}
                />
            : <LabelValueListItem 
                label="Magical Damage" 
                value={`${this.phMin} ~ ${this.phMax}`}
              />
          }
    
          <LabelValueListItem 
            label={"Attack Speed"}
            value={`${this.attackSpeed/1000}s`}
          />

          <LabelValueListItem 
            label={"Range"}
            value={`${this.range/100}m`}
          />

        </>
      )
    }
    else if (["coat", "pants", "gauntlet", "shoes"].includes(table)) {
      this.phDef = data.physical_defense;
      this.mgDef = data.magic_defense;
      
      var stats = (
        <>
          {table == "coat"
            ? <LabelValueListItem 
                label="Physical Defense"
                value={Math.floor(this.phDef + upgradeData[this.state.upgradeLevel].value_0).toString()}
                valueClassName={`upgrade-${this.state.upgradeLevel}`}
              />
            : <LabelValueListItem 
                label="Physical Defense"
                value={this.phDef}
              />
          }

          {table == "pants"
            ? <LabelValueListItem
                label="Magical Defense"
                value={Math.floor(this.mgDef + upgradeData[this.state.upgradeLevel].value_0).toString()}
                valueClassName={`upgrade-${this.state.upgradeLevel}`}
              />
            : <LabelValueListItem 
                label="Magical Defense"
                value={this.mgDef}
              />
          }

          {table == "gauntlet" &&
            <>
              <LabelValueListItem 
                label="Hitrate"
                value={Math.floor(0 + upgradeData[this.state.upgradeLevel].value_0).toString()}
                valueClassName={`upgrade-${this.state.upgradeLevel}`}
              />

              <LabelValueListItem 
                label="Attack Speed"
                value={`${this.state.upgradeLevel}%`}
                valueClassName={`upgrade-${this.state.upgradeLevel}`}
              />
            </>
          }

          {table == "shoes" &&
            <>
              <LabelValueListItem 
                label="Avoidance Rate"
                value={Math.floor(0 + upgradeData[this.state.upgradeLevel].value_0).toString()}
                valueClassName={`upgrade-${this.state.upgradeLevel}`}
              />

              <LabelValueListItem 
                label="Moving Speed"
                value={`${this.state.upgradeLevel}%`}
                valueClassName={`upgrade-${this.state.upgradeLevel}`}
              />
            </>
          }

        </>
      )
    }
    else {
      return null;
    }

    return (
      <CardList header={true} list={true}>
        <span className="card-title">Upgrade</span>

        <div style={{display: "flex", paddingTop: "15px", paddingLeft: "20px", paddingRight: "20px"}}>
          <span>{this.state.upgradeLevel}</span>
          <input 
            className="upgrade-slider"
            type="range"
            onChange={e => this.setState({upgradeLevel: parseInt(e.target.value)})}
            min="0"
            max="15"
            value={this.state.upgradeLevel}
          />
        </div>

        {stats}

      </CardList>
    )
  }
}