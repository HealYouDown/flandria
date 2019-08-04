import React from "react";

export default class Icon extends React.Component {
  render() {
    const {
      table,
      data,
      normalProductBookIcon,
      npc
    } = this.props;
    
    const iconPath = data.rating_type != undefined ? "/static/img/monster_icons/" : "/static/img/item_icons/";

    if (table == "quest") {
      return null;
    }

    if (npc) {
      return (
        <img 
          style={{alignSelf: "center", flexGrow: 0, marginRight: "5px"}}
          src={"/static/img/npc_icons/" + data.icon} 
        />
      )
    }

    if (!normalProductBookIcon && table == "product_book") {
      return (
        <img
          style={{alignSelf: "center", flexGrow: 0, marginRight: "5px"}}
          src={iconPath + data.target.result_item.icon} 
        />
      )
    }

    return (
      <img 
        style={{alignSelf: "center", flexGrow: 0, marginRight: "5px"}}
        className="icon" src={iconPath + data.icon}
      />
    )
  }
}
