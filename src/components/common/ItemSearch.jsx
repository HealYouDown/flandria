import React, { useState } from "react";
import { useDebouncedCallback } from "use-debounce";
import styled from "styled-components";
import { BLUE } from "../colors";
import { searchDatabase } from "../fetch";
import Icon from "./Icon";
import Name from "./Name";
import RightArrow from "../common/RightArrow";
import { map } from "../breakpoint";

const SearchWrapper = styled.div`
  display: flex;
  flex-flow: column;
  justify-content: center;
  ${map({"sm": "10%", "md": "15%", "lg": "25%"}, val => `padding: 30px ${val};`)}
`;

const ItemSearchInput = styled.input`
  flex-grow: 1;
  border: none;
  background: rgba(0, 0, 0, 0.5);
  font-size: 18px;
  padding: 12px 20px;
  border-top-left-radius: 3px;
  border-top-right-radius: 3px;
  border: 1px solid black;

  &:hover {
    background: rgba(0, 0, 0, 0.7);
  }

  &:active, &:focus {
    background: rgba(0, 0, 0, 0.7);
    color: ${BLUE};
  }
`

const ResultsWrapper = styled.div`
  flex-grow: 1;
  display: flex;
  flex-flow: column;
  max-height: 200px;
  overflow-y: auto;
  position: relative;
  background: rgba(0, 0, 0, 0.5);
`

const ResultItemWrapper = styled.div`
  display: flex;
  flex-flow: row;
  padding: 4px 12px;
  cursor: pointer;

  &:not(:first-child) {
    border-top: 1px solid black;
  }

  &:hover {
    background: rgba(0, 0, 0, 0.3);

    .right-arrow path {
      fill: white;
    }
  }

  > div {
    flex-grow: 1;
    display: flex;
    flex-flow: row;
    align-items: center;
  }
`

const ResultItem = ({item, callback}) => {
  return (
    <ResultItemWrapper onClick={() => callback(item)}>
      <div>
        <Icon tablename={item.table} icon={item.icon} />
        <Name tablename={item.table} data={item} />
      </div>
      <RightArrow />
    </ResultItemWrapper>
  )
}

const ItemSearch = ({callback}) => {
  const [results, setResults] = useState([]);

  const [debouncedSearchCallback] = useDebouncedCallback((value) => {
    if (value.length == 0) {
      setResults([]);
      return;
    }
  
    searchDatabase(value)
      .then(res => res.json())
      .then(json => {
        setResults(json);
      });
  }, 300);


  return (
    <SearchWrapper>
      <ItemSearchInput
        fontsize={18}
        onChange={e => debouncedSearchCallback(e.target.value)}
        placeholder="Search Database"
      />
      {results.length > 0 && (
        <ResultsWrapper>
          {results.map(item => <ResultItem callback={callback} item={item} />)}
        </ResultsWrapper>
      )}
    </SearchWrapper>
  )

}

export default ItemSearch;