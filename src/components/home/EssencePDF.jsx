import React from "react";
import { Redirect } from "react-router-dom";

export default class EssencePDF extends React.Component {
  componentDidMount() {
    const params = new URLSearchParams(location.search);
    const lang = params.get("lang") || "en";
    window.open(`/static/files/essence_system_${lang}.pdf`);
  }

  render() {
    return (
      <Redirect to="/" />
    )
  }
}