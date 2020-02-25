import React, { useState, useEffect } from "react";
import { TextInput } from "../common/Inputs";
import styled from "styled-components";
import Select from "react-select";
import "../../styles/react-select.css";
import history from "../history";
import breakpoint from "../breakpoint";
import { bonusCodes } from "../bonus_codes";
import { BLUE } from "../colors";
import { useDebouncedCallback } from "use-debounce";


const Wrapper = styled.div`
  display: flex;
  flex-flow: row;
  flex-wrap: none;

  > input {
    flex-grow: 1;
  }
`

const FilterWrapper = styled.div`
  display: ${props => props.visible ? "grid" : "none"};
  grid-column-gap: 15px;
  grid-row-gap: 10px;
  ${breakpoint("sm")`
    grid-template-columns: auto;
  `}
  ${breakpoint("md")`
    grid-auto-flow: column;
  `}
  ${breakpoint("lg")`
    grid-auto-flow: column;
  `}
  ${breakpoint("xl")`
    grid-auto-flow: column;
  `}

  padding: 10px 10px;

  > div {
    width: 100%
  }
`

const FilterButton = styled.button`
  border: none;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 5px 15px;
  margin-left: 5px;
  cursor: pointer;
  transition: color 0.3s;
  border-radius: 3px;
  font-size: 17px;

  &:hover {
    background-color: rgba(0, 0, 0, 0.7);
    color: ${BLUE};
  }
`

const MySelect = ({options, currentValue, keyname, changeState}) => {
  return (
    <Select
      options={options}
      value={options.filter(o => o.value === currentValue)}
      className="react-container"
      classNamePrefix="react-select"
      onChange={event => {
        const newState = {[keyname]: event.value};
        // filters that change the numbers of items will
        // reset page to 1
        if (keyname == "filter" || keyname == "location") {
          newState.page = 1;
        }
        changeState(newState);
      }}
    />
  )
}

const OverviewFilter = ({
  tablename,
  changeState,
  order,
  sort,
  filter,
  location,
  search,
  bonuses,
}) => {
  const [filterShown, setFilterShown] = useState(false);

  const [debouncedSearchCallback] = useDebouncedCallback((value) => {
    /// This will trigger __ms (see above) after setSearchTerm
    /// was called. Delayed search to not search after every typestroke.
    changeState({search: value, page: 1})
  }, 300)

  const weaponTables = [
    "cariad", "rapier", "dagger", "one_handed_sword",
    "two_handed_sword", "rifle", "duals"
  ];
  const armorTables = [
    "shield", "pants", "coat", "shoes", "gauntlet"
  ];
  const tablesWithLocationFilter = ["monster", "quest"];
  const tablesWithBonusFilter = ["dress", "hat", "accessory"];

  // Filter Options
  const orderOptions = [
    { label: "Ascending", value: "asc" },
    { label: "Descending", value: "desc" }
  ];

  // Sort Options
  const sortOptions = [
    { label: "Added", value: "added" },
    { label: "Name", value: "name" },
  ];
  if (tablename === "monster") {
    sortOptions.push(...[
      { label: "Level", value: "level" },
      { label: "HP", value: "hp" },
      { label: "Experience", value: "experience" },
      { label: "Min. Dmg", value: "min_dmg" },
      { label: "Max. Dmg", value: "max_dmg" },
    ])
  } else if (tablename === "quest") {
    sortOptions.push(...[
      { label: "Level", value: "level" }
    ])
  } else if (tablename === "accessory") {
    sortOptions.push(...[
      { label: "Level", value: "level_land"}
    ])
  } else if (weaponTables.includes(tablename) || armorTables.includes(tablename)) {
    sortOptions.push(...[
      { label: "Land Level", value: "level_land" },
      { label: "Sea Level", value: "level_sea" }
    ])
  }

  // Filter Options
  const filterOptions = [
    { label: "All", value: "all"}
  ];
  if (tablename === "monster") {
    filterOptions.push(...[
      { label: "Normal Monster", value: "rating_type:0" },
      { label: "Elite Monster", value: "rating_type:1" },
      { label: "Boss", value: "rating_type:2" },
      { label: "Endboss", value: "rating_type:3" },
    ])
  } else if (weaponTables.includes(tablename) || armorTables.includes(tablename)) {
    filterOptions.push(...[
      { label: "Noble", value: "class_land:Noble" },
      { label: "Magic Knight", value: "class_land:Magic Knight" },
      { label: "Court Magician", value: "class_land:Court Magician" },
      { label: "Mercenary", value: "class_land:Mercenary" },
      { label: "Gladiator", value: "class_land:Gladiator" },
      { label: "Guardian Swordman", value: "class_land:Guardian Swordsman" },
      { label: "Saint", value: "class_land:Saint" },
      { label: "Priest", value: "class_land:Priest" },
      { label: "Shaman", value: "class_land:Shaman" },
      { label: "Explorer", value: "class_land:Explorer" },
      { label: "Excavator", value: "class_land:Excavator" },
      { label: "Sniper", value: "class_land:Sniper" },
    ])
  }

  // Location options
  const locationOptions = [
    { label: "Both", value: "location:-1" },
    { label: "Land", value: "location:0" },
    { label: "Sea", value: "location:1" }
  ];

  // Bonus options
  const bonusOptions = [];
  Object.keys(bonusCodes).forEach(bonusId => {
    bonusOptions.push({ label: bonusCodes[bonusId], value: bonusId });
  })

  // Creates filter that are shown
  const filterList = [];
  // Every item has sort by and order
  filterList.push(
    <MySelect
      options={orderOptions}
      currentValue={order}
      changeState={changeState}
      keyname="order"
    />
  );

  filterList.push(
    <MySelect
      options={sortOptions}
      currentValue={sort}
      changeState={changeState}
      keyname="sort"
    />
  );

  // Check if filter has any items except all
  if (Object.keys(filterOptions).length >= 2) {
    filterList.push(
      <MySelect
        options={filterOptions}
        currentValue={filter}
        changeState={changeState}
        keyname="filter"
      />
    );
  }

  // Location filter
  if (tablesWithLocationFilter.includes(tablename)) {
    filterList.push(
      <MySelect
        options={locationOptions}
        currentValue={location}
        changeState={changeState}
        keyname="location"
      />
    );
  }

  if (tablesWithBonusFilter.includes(tablename)) {
    filterList.push(
      <Select
        isMulti={true}
        isSearchable={true}
        options={bonusOptions}
        value={bonusOptions.filter(option => bonuses.includes(parseInt(option.value)))}
        className="react-container"
        classNamePrefix="react-select"
        onChange={selected => {
          let selectedBonusCodes = [];
          if (selected) {
            selected.forEach(bonusOption => selectedBonusCodes.push(parseInt(bonusOption.value)));
          }
          changeState({bonuses: selectedBonusCodes})
        }}
      />
    );
  }

  return (
    <>
      <Wrapper>
        <TextInput
          fontsize={18}
          placeholder="Search…"
          type="text"
          defaultValue={search}
          onChange={e => debouncedSearchCallback(e.target.value)}
        />
        <FilterButton onClick={() => setFilterShown(!filterShown)}>Filter</FilterButton>
      </Wrapper>
      <FilterWrapper visible={filterShown}>
        {filterList}
      </FilterWrapper>
    </>
  )
}

export default OverviewFilter;