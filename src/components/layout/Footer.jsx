import React from "react";
import styled, { css } from "styled-components";
import { Link } from "react-router-dom";
import { BLUE } from "../colors";

const FooterWrapper = styled.div`
  padding: 10px 0px;
  background: rgba(0, 0, 0, 0.7);
  /*border-top-left-radius: 30%;
  border-top-right-radius: 30%;*/
  display: flex;
  flex-flow: column;
  justify-content: center;
  align-items: center;
`

const CopyrightClaim = styled.div`
  background: black;
  display: flex;
  flex-flow: row;
  justify-content: center;
  align-items: center;

  > span {
    font-size: 12px;
    color: #aaa;
  }
`

const FooterLinksWrapper = styled.div`
  display: flex;
  flex-flow: row;
`

const FooterLink = styled(Link)`
  text-decoration: none;
  padding: 5px 8px;
  font-size: 12px;
  transition: color 0.25s;
  cursor: pointer;
  color: #aaa;

  &:hover {
    color: ${BLUE};
  }
`

const OutsideFooterLink = styled.a`
  text-decoration: none;
  padding: 5px 8px;
  font-size: 12px;
  transition: color 0.25s;
  cursor: pointer;
  color: #aaa;

  &:hover {
    color: ${BLUE};
  }
`

const Footer = () => {
  return (
    <footer>
      <FooterWrapper>
        <FooterLinksWrapper>
          <FooterLink to="/about">About</FooterLink>
          <FooterLink to="/privacy">Privacy Policy</FooterLink>
          <OutsideFooterLink target="_blank" href="https://github.com/HealYouDown/flandria">Github</OutsideFooterLink>
          <OutsideFooterLink target="_blank" href="https://discord.gg/zDax9Rg">Discord</OutsideFooterLink>
        </FooterLinksWrapper>
        <FooterLinksWrapper>
          <OutsideFooterLink target="_blank" href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DWR39ZZHBKXAQ&source=url">Paypal</OutsideFooterLink>
          <OutsideFooterLink target="_blank" href="https://www.patreon.com/flandria">Patreon</OutsideFooterLink>
        </FooterLinksWrapper>
      </FooterWrapper>
      <CopyrightClaim>
        <span>© 2020 Flandria.info</span>
      </CopyrightClaim>
    </footer>
  )
}

export default Footer;