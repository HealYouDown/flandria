import React from "react";
import { Redirect } from "react-router-dom";

export default class EssencePDF extends React.Component {
  componentDidMount() {
    window.open("/static/files/FLORENSIA-EssenceSystem_Explaination.pdf");
  }

  render() {
    return (
      <Redirect to="/" />
    )
  }
}