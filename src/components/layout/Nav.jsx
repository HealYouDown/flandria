import React, { useState } from "react";
import { Link } from "react-router-dom";
import * as S from "./NavStyles";
import { Visible, Hidden } from "../common/Visible";
import HamburgerMenu from "react-hamburger-menu";
import { isLoggedIn, getName, logoutUser } from "../auth/auth";


const Navigation = () => {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn());
  // Desktop State
  const [hovered, setHovered] = useState(false);
  const [activeHover, setActiveHover] = useState("");
  // Mobile state
  const [hamburgerOpen, setHamburgerOpen] = useState(false);

  const preventRouting = (event) => {
    event.preventDefault();
  }

  const hover = (activeHover) => {
    setHovered(true);
    setActiveHover(activeHover);
  }

  const unHover = () => {
    setHovered(false);
    setActiveHover("");
  }

  const closeHamburger = () => {
    setHamburgerOpen(false);
  }

  const updateUserState = () => {
    setLoggedIn(isLoggedIn());
  }

  window.addEventListener("storage", updateUserState);

  return (
    <S.Nav>

      <Link onClick={unHover} onClick={closeHamburger} to="/">
        <S.BrandImage src="/static/assets/logo.png" />
      </Link>

      <Visible breakpoint="md">
        <S.NavLinkWrapper>
          <S.NavLink
            onClick={unHover}
            onMouseEnter={unHover}
            to="/database/monster"
          >
            Monster
          </S.NavLink>
          <S.NavLink
            onClick={unHover}
            onMouseEnter={unHover}
            to="/database"
          >
            Items
          </S.NavLink>
          <S.NavLink
            onClick={unHover}
            onMouseEnter={unHover}
            to="/map"
          >
            Maps
          </S.NavLink>
          <S.NavLink onClick={unHover} onMouseEnter={unHover} to="/database/quest">Quests</S.NavLink>
          <S.NavLink onClick={unHover} onMouseEnter={unHover} to="/ranking/guild">Guilds</S.NavLink>

          <S.NavLink to="/" onClick={preventRouting} onMouseEnter={() => hover("planner")}>
            Planner
            <S.NavDropdownList visible={(hovered && activeHover == "planner")}>
              <S.NavDropdownLink onClick={unHover} to="/planner/noble">Noble</S.NavDropdownLink>
              <S.NavDropdownLink onClick={unHover} to="/planner/explorer">Explorer</S.NavDropdownLink>
              <S.NavDropdownLink onClick={unHover} to="/planner/saint">Saint</S.NavDropdownLink>
              <S.NavDropdownLink onClick={unHover} to="/planner/mercenary">Mercenary</S.NavDropdownLink>
              <S.NavDropdownLink onClick={unHover} to="/planner/ship">Ship</S.NavDropdownLink>
            </S.NavDropdownList>
          </S.NavLink>

          {loggedIn ? (
            <S.NavLink to="/" onClick={unHover} onClick={preventRouting} onMouseEnter={() => hover("account")}>
              {getName()}
              <S.NavDropdownList visible={(hovered && activeHover == "account")}>
                <S.NavDropdownLink onClick={e => {e.preventDefault(); unHover(); logoutUser();}} to="/auth/logout">Logout</S.NavDropdownLink>
              </S.NavDropdownList>
            </S.NavLink>
          ) : (
            <S.NavLink onClick={unHover} onMouseEnter={unHover} to="/auth/login">Login</S.NavLink>
          )}

        </S.NavLinkWrapper>
      </Visible>

      <Hidden breakpoint="md">
        <S.HamburgerMenuWrapper>
          <HamburgerMenu
            isOpen={hamburgerOpen}
            menuClicked={() => setHamburgerOpen(!hamburgerOpen)}
            width={28}
            height={20}
            strokeWidth={3}
            borderRadius={5}
            color="white"
          />
        </S.HamburgerMenuWrapper>
       
        <S.HamburgerMenuBackdrop visible={hamburgerOpen} />
        
        <S.HamburgerMenuLinkWrapper visible={hamburgerOpen}>
          <S.HamburgerMenuLink onClick={closeHamburger} to="/database/monster">Monster</S.HamburgerMenuLink>
          <S.HamburgerMenuLink onClick={closeHamburger} to="/database">Items</S.HamburgerMenuLink>
          <S.HamburgerMenuLink onClick={closeHamburger} to="/map">Maps</S.HamburgerMenuLink>
          <S.HamburgerMenuLink onClick={closeHamburger} to="/database/quest">Quests</S.HamburgerMenuLink>
          <S.HamburgerMenuLink onClick={closeHamburger} to="/ranking/guild">Guilds</S.HamburgerMenuLink>
          <S.HamburgerParentLink>
            Planner
            <S.HamburgerMenuChildLink onClick={closeHamburger} to="/planner/noble">Noble</S.HamburgerMenuChildLink>
            <S.HamburgerMenuChildLink onClick={closeHamburger} to="/planner/explorer">Explorer</S.HamburgerMenuChildLink>
            <S.HamburgerMenuChildLink onClick={closeHamburger} to="/planner/saint">Saint</S.HamburgerMenuChildLink>
            <S.HamburgerMenuChildLink onClick={closeHamburger} to="/planner/mercenary">Mercenary</S.HamburgerMenuChildLink>
            <S.HamburgerMenuChildLink onClick={closeHamburger} to="/planner/ship">Ship</S.HamburgerMenuChildLink>
          </S.HamburgerParentLink>
          {loggedIn ? (
            <S.HamburgerParentLink>
              {getName()}
              <S.HamburgerMenuChildLink onClick={e => {e.preventDefault(); closeHamburger(); logoutUser();}} to="/auth/logout">Logout</S.HamburgerMenuChildLink>
            </S.HamburgerParentLink>
          ) : (
            <S.HamburgerMenuLink onClick={closeHamburger} to="/auth/login">Login</S.HamburgerMenuLink>
          )}
        </S.HamburgerMenuLinkWrapper>
      </Hidden>

      <S.NavBackgroundDropdown
        open={hovered}
      />
      {hovered && (
        <S.NavBackgroundDropdownReset
          onMouseEnter={unHover}
        />
      )}
  
    </S.Nav>
  )
}

export default Navigation;