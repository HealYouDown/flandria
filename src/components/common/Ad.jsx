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
        style={{ display: 'inline-block', width: "100%" }}
        data-ad-client='ca-pub-7852193310298972'
        data-ad-slot={this.props.slot}
      />
    );
  }
}