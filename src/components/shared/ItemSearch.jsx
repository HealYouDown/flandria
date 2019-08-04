import React from "react";
import Icon from "../database/Icon";
import Name from "../database/Name";
import AuthService from "../AuthService";

import "./ItemSearch.css";

export default class ItemSearch extends React.Component {
  constructor(props) {
    super(props);
    this.auth = new AuthService();

    this.state = {
      results: [],
      focus: false,
    }

    this._handleSearchChange = this._handleSearchChange.bind(this);
  }

  _handleSearchChange(event) {
    let searchString = event.target.value;

    this.auth.fetch("GET", "search", {
      query: `s=${searchString}`
    })
    .then(res => {
      if (res.error) {
        alert(res.errorMessage);
      }
      else {
        this.setState({results: res.body});
      }
    })
  }

  render() {
    const {
      results,
      focus,
    } = this.state;

    const {
      searchInputWrapperStyle,
      searchInputStyle,
      clickAction
    } = this.props;

    var searchResultsHeight = 0;
    if (focus) {
      if (results.length < 10) {
        searchResultsHeight = results.length * 34
      }
      else {
        searchResultsHeight = 300;
      }
    }

    return (
      <div style={searchInputWrapperStyle}>
        <input 
          onBlur={() => {this.setState({focus: false})}} 
          onFocus={() => {this.setState({focus: true})}} 
          onChange={this._handleSearchChange} 
          className="search-input" 
          type="search" 
          placeholder="Search Database"
          style={searchInputStyle}
        />

        <ul style={{height: `${searchResultsHeight}px`}} className="search-results reset">
          {results.map((item, i) => {
            return (
              <li key={i} onMouseDown={() => clickAction(item)} className="search-list-item">
                <div style={{display: "flex"}}>
                  <Icon normalProductBookIcon={true} table={item.table} data={item} />
                  <Name normalProductBookColor={true} table={item.table} data={item} />
                </div>
              </li>
            )
          })}
        </ul>
      </div>
    )
  }
}