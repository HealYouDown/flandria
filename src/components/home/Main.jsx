import React from "react";
import ItemSearch from "../common/ItemSearch";
import history from "../history";


const Main = () => {
  const itemSearchCallback = (item) => {
    history.push(`/database/${item.table}/${item.code}`);
  }

  document.title = "Home";

  return (
    <ItemSearch callback={itemSearchCallback} />
  )
}

export default Main;