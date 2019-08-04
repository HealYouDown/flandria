import React from "react";

export default class NoMatch extends React.Component {
  componentDidMount() {
    throw Error("Site was not found.")
  }

  render() { // Will never be executed
    return (<></>)
  }
}