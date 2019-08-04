import React from "react";
import { Link } from "react-router-dom";
import RightArrow from "./RightArrow";

import "./CardList.css";

class CardList extends React.Component {
  constructor(props) {
    super(props);

    this.list = this.props.list;
    this.state = {
      bodyItems: this._getBodyItems(this.props)
    }
  }

  _getBodyItems(props) {
    let bodyItems = props.children
    if (props.header) {
      bodyItems = props.children.slice(1);
    }
    return bodyItems;
  }

  componentWillReceiveProps(nextProps) {
    this.setState({
      bodyItems: this._getBodyItems(nextProps),
    })
  }

  render() {
    const {
      bodyItems,
    } = this.state;

    var body;
    if (this.list) {
      body = (
        <ul className="card-body reset" style={{padding: `${this.props.padding}px`}}>
          {bodyItems}
        </ul>
      )
    }
    else {
      body = (
        <div className="card-body" style={{padding: `${this.props.padding}px`}}>
          {bodyItems}
        </div>
      )
    }

    return (
      <div className="card">
        {this.props.header && (
          <div className="card-header">
            {this.props.children[0]}
          </div>
        )}

        {body}
      </div>
    )
  }
}

class ClickableListItem extends React.Component {
  constructor(props) {
    super(props);

    this.hover = this.props.hover;
  }

  render() {
    let className = "clickable-list-item clickable-list-item-link"
    if (this.hover != undefined && !this.hover) {
      className += " no-hover"
    }
    return (
      <li>
        <Link className={className} to={this.props.link}>
          <div className="center">
            {this.props.children}
          </div>
          <RightArrow />
        </Link>
      </li>
    )
  }
}

class LabelValueListItem extends React.Component {
  render() {
    const {
      label,
      value,
      valueClassName
    } = this.props;

    return (
      <li className="label-value-list-item">
        <span>{label}</span>
        <span className={valueClassName}>{value}</span>
      </li>
    )
  }
}


export default CardList;
export {
  ClickableListItem,
  LabelValueListItem
}