import React from "react";

export default class Ad extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    (window.adsbygoogle = window.adsbygoogle || []).push({});
  }

  render() {
    return (
      <ins className='adsbygoogle'
        style={{ display: 'inline-block', minWidth: "400px", width: "100%", height: "100px", marginTop: "15px" }}
        data-ad-client='ca-pub-7852193310298972'
        data-ad-slot={this.props.slot}
      />
    );
  }
}