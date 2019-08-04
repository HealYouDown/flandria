import React from "react";
import CardList, { LabelValueListItem } from "../../shared/CardList";
import Icon from "../Icon";
import Name from "../Name";

import "./Infos.css";

export default class Infos extends React.Component {
  render() {
    const {
      table,
      data,
      itemInfos
    } = this.props;

    return (
      <CardList header={true} list={true}>

        <div className="info-header">
          <Icon table={table} data={data} normalProductBookIcon={true} />
          <Name table={table} data={data} normalProductBookColor={true} />
        </div>

        {itemInfos.map((info, index) => {
          return <LabelValueListItem key={index} label={info.label} value={info.value} />
        })}

      </CardList>
    )
  }
}