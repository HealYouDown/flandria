import React from "react";
import { Redirect } from "react-router-dom";

export default class EssencePDF extends React.Component {
  constructor(props) {
    super(props);
    this.lang = props.match.params.lang;
  }

  componentDidMount() {
    window.open(`/static/files/essence_system_${this.lang}.pdf`);
  }

  render() {
    return (
      <Redirect to="/" />
    )
  }
}