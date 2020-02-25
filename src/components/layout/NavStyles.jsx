import styled, { css } from "styled-components";
import { Link } from "react-router-dom";
import { BLUE } from "../colors";

const Nav = styled.nav`
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
  padding: 10px 15px;
  position: relative;
  z-index: 5;
`

const BrandImage = styled.img`
  height: 50px;
  width: auto;
  position: relative;
  z-index: 5;
`

const NavLinkWrapper = styled.div`
  display: flex;
  flex-flow: row;
  flex-wrap: nowrap;
`

const NavLinkStyle = css`
  font-size: 18px;
  letter-spacing: 1.1px;
  cursor: pointer;
  padding: 10px 20px;
  text-decoration: none;
  transition: color 0.3s;
  transition: border-top-color 0.2s;
  color: #aaa;
  border-top: 1px solid #aaa;

  &:hover {
    color: ${BLUE};
    border-top-color: ${BLUE};
  }
`

const NavLink = styled(Link)`
  ${NavLinkStyle}
`

const NavBackgroundDropdown = styled.div`
  position: absolute;
  left: 0;
  top: 0;
  right: 0;
  z-index: -1;
  background: rgba(0, 0, 0, 0.7);
  transition: height 0.35s ease;
  height: ${props => props.open ? "200px" : "0px"};
`

const NavBackgroundDropdownReset = styled.div`
  position: fixed;
  z-index: -2;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: transparent;
  pointer-events: auto;
`

const NavDropdownList = styled.div`
  position: absolute;
  margin: 0;
  padding: 0;
  margin-top: 10px;
  display: flex;
  flex-flow: column;
  flex-wrap: nowrap;
  transition: 0.1s visibility 0s, opacity 0.3s;
  ${props => props.visible
    ? {
      opacity: 1,
      visibility: "visible",
    }
    : {
      transition: "none",
      opacity: 0,
      visibility: "hidden",
    }
  }
`

const NavDropdownLink = styled(Link)`
  ${NavLinkStyle};
  border-top: none;
  font-size: 16px;
  margin: 0;
  padding: 0;
`

const HamburgerMenuWrapper = styled.div`
  margin-top: 10px;
  margin-right: 5px;
`

const HamburgerMenuBackdrop = styled.div`
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
  background: rgba(0, 0, 0, 0.8);
  transition: opacity 0.15s ease-in-out;
  opacity: ${props => props.visible ? 0.7 : 0};
  pointer-events: ${props => props.visible ? "auto": "none"};
`

const HamburgerMenuLinkWrapper = styled.div`
  display: ${props => props.visible ? "block" : "none"};
  position: absolute;
  z-index: 100;
  left: 0;
  top: 0;
  margin-left: 30px;
  margin-top: 80px;
`

const hamburgerLinkStyle = css`
  display: block;
  font-size: 18px;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.3s;
  letter-spacing: 1.3px;
  color: #aaa;

  &:hover {
    color: ${BLUE};
  }
`

const HamburgerMenuLink = styled(Link)`
  ${hamburgerLinkStyle};
`

const HamburgerParentLink = styled.span`
  ${hamburgerLinkStyle};
`

const HamburgerMenuChildLink = styled(Link)`
  ${hamburgerLinkStyle};
  font-size: 14px;
  letter-spacing: 1.1px;
  padding-left: 20px;
`

export {
  Nav, BrandImage, NavLinkWrapper, NavLink, NavBackgroundDropdown,
  NavBackgroundDropdownReset, NavDropdownList, NavDropdownLink,
  HamburgerMenuWrapper, HamburgerMenuBackdrop, HamburgerMenuLinkWrapper,
  HamburgerMenuLink, HamburgerMenuChildLink, HamburgerParentLink
}