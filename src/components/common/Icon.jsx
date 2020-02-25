import React from "react";
import styled from "styled-components";

const Image = styled.img`
  align-self: center;
  flex-grow: 0;
  margin-right: 5px;
  max-width: 32px;
  max-height: auto;
  border-radius: 50%;
  /*border: 2px solid black*/;
`

const Icon = ({tablename, icon}) => {
  if (tablename == "quest") {
    return null;
  }

  let sourceFolder;
  if (tablename == "npc") {
    sourceFolder = "npc_icons";
  } else {
    sourceFolder = tablename == "monster" ? "monster_icons" : "item_icons";
  }

  return <Image src={`/static/assets/${sourceFolder}/${icon}`} />
}

export default Icon;