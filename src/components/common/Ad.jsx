import React from "react";
import styled from "styled-components";

const AdblockBannerWrapper = styled.div`
  width: auto;
  margin-top: 15px;
  margin-left: 30px;
  margin-right: 30px;
  background: rgba(0, 0, 0, 0.6);
  border-radius: 10px;
  padding: 15px 40px;

  span {
    display: block;
  }

  > span:first-child {
    text-align: center;
    color: orange;
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 7px;
  }

  > span:last-child {
    text-align: center;
  }
`

export default class Ad extends React.Component {
  constructor(props) {
    super(props);
    this.adblockerEnabled = window.canRunAds === undefined;
  }

  componentDidMount() {
    if (!this.adblockerEnabled) {
      (window.adsbygoogle = window.adsbygoogle || []).push({});
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    }
  }

  render() {

    if (!this.adblockerEnabled) {
      return (
        <div style={{marginTop: "15px"}}>
          <ins className='adsbygoogle'
            style={{ display: 'inline-block', width: "50%", height: "100px" }}
            data-ad-client='ca-pub-7852193310298972'
            data-ad-slot={this.props.slot}
          />
          <ins className='adsbygoogle'
            style={{ display: 'inline-block', width: "50%", height: "100px" }}
            data-ad-client='ca-pub-7852193310298972'
            data-ad-slot={this.props.slot}
          />
        </div>
      );
    }

    return (
      <AdblockBannerWrapper>
        <span>I would be an Ad.</span>
        <span>If you want to support Flandria, please disable your adblocker or whitelist our page. We won't show any popups or annoying videos - just a banner at the bottom. Thanks!</span>
      </AdblockBannerWrapper>
    )
  }
}