import React from "react";
import "../../../styles/forms.css";
import Select from "react-select";
import { tableToFilters } from "../../../constants/filters";
import { bonusCodes } from "../../../constants/bonus_codes";
import { FaFilter } from "react-icons/fa";
import { Row, Col } from "react-grid-system";
import "./FilterMenu.css"
import "../../../styles/react-select-override.css";

export default class FilterMenu extends React.Component {
  render() {
    const {
      changeState,
      table,
      filterVisible,
      searchString,
      order,
      sortBy,
      filterBy,
      location,
      selectedBonusCodes,
    } = this.props;

    // Filter data
    const tableFilterData = tableToFilters[table] || {}

    const locationFilter = tableFilterData["location"] == true ? true : false;
    const filterData = tableFilterData["filter"] || {};
    const sortData = tableFilterData["sort"] || {};
    const bonusFilter = tableFilterData["bonus"] == true ? true : false;

    // Col width calculation
    var numberOfFilters = 2;
    if (locationFilter) {
      numberOfFilters++;
    }
    if (Object.keys(filterData).length >= 1) {
      numberOfFilters++;
    }

    var colWidth;
    var bonusColWidth;
    if (bonusFilter) {
      colWidth = 2;
      bonusColWidth = 12 - numberOfFilters * 2;
    }
    else {
      colWidth = Math.floor(12 / numberOfFilters);
    }

    // Options

    // Order Options
    const orderOptions = [
      { label: "Asc", value: "asc" },
      { label: "Desc", value: "desc" }
    ];

    // Location Options
    const locationOptions = [
      { label: "Both", value: "location:-1" },
      { label: "Land", value: "location:0" },
      { label: "Sea", value: "location:1" }
    ];

    // Filter Options
    const filterOptions = [
      { label: "All", value: "all" }
    ];
    Object.keys(filterData).map(key => {
      filterOptions.push({ label: key, value: filterData[key] })
    });

    // Sort Options
    const sortOptions = [
      { label: "Added", value: "added" },
      { label: "Name", value: "name" },
    ];
    Object.keys(sortData).map(key => {
      sortOptions.push({ label: key, value: sortData[key] })
    });

    // Bonus Options
    const bonusOptions = [];
    Object.keys(bonusCodes).map(c => {
      bonusOptions.push({ label: bonusCodes[c], value: parseInt(c) });
    })

    return (
      <>
        <div className="search-wrapper">
          <input 
            className="search-input form-input input-style" 
            type="search"
            value={searchString}
            onChange={e => changeState({searchString: e.target.value})}
          />
          <button
            className="filter-button"
            onClick={e => changeState({filterVisible: !filterVisible})}
          >
            <FaFilter />
            <span>Filter</span>
          </button>
        </div>

        {filterVisible && (
          <Row className="filter-menu" justfiy="center">

            <Col md={colWidth}>
              <label className="react-container-label">Order</label>
              <Select
                value={orderOptions.filter(option => option.value == order)}
                options={orderOptions}
                onChange={selected => changeState({order: selected.value})}
                isSearchable={false}
                className="react-container"
                classNamePrefix="react-select"
              />
            </Col>

            <Col md={colWidth}>
              <label className="react-container-label">Sort by</label>
              <Select
                value={sortOptions.filter(option => option.value == sortBy)}
                options={sortOptions}
                onChange={selected => changeState({sortBy: selected.value})}
                isSearchable={false}
                className="react-container"
                classNamePrefix="react-select"
              />
            </Col>

            {Object.keys(filterData).length >= 1 &&
              <Col md={colWidth}>
                <label className="react-container-label">Filter by</label>
                <Select
                  value={filterOptions.filter(option => option.value == filterBy)}
                  options={filterOptions}
                  onChange={selected => changeState({filterBy: selected.value})}
                  isSearchable={false}
                  className="react-container"
                  classNamePrefix="react-select"
                />
              </Col>
            }

            {locationFilter &&
              <Col md={colWidth}>
                <label className="react-container-label">Location</label>
                <Select
                  value={locationOptions.filter(option => option.value == location)}
                  options={locationOptions}
                  onChange={selected => changeState({location: selected.value})}
                  isSearchable={false}
                  className="react-container"
                  classNamePrefix="react-select"
                />
              </Col>
            }

            {bonusFilter &&
              <Col md={bonusColWidth}>
                <label className="react-container-label">Bonus stats</label>
                <Select
                  value={bonusOptions.filter(b => selectedBonusCodes.includes(b.value))}
                  options={bonusOptions}
                  onChange={selected => {
                    let selectedBonusCodes = [];
                    if (selected) {
                      selected.forEach(s => selectedBonusCodes.push(parseInt(s.value)))
                      changeState({selectedBonusCodes: selectedBonusCodes})
                    }
                    else {
                      changeState({selectedBonusCodes: []})
                    }
                  }}
                  isSearchable={true}
                  isMulti={true}
                  isClearable={true}
                  className="react-container"
                  classNamePrefix="react-select"
                />
              </Col>
            }

          </Row>
        )}
      </>
    )
  }
}