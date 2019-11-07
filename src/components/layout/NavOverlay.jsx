import React from "react";
import { Link } from "react-router-dom";

import "./HamburgerIcon.css";
import "./NavOverlay.css";
import AuthService from "../AuthService";

export default class NavOverlay extends React.Component {
  constructor(props) {
    super(props);
    this.auth = new AuthService();

    this.state = {
      open: false,
      actives: [],
    }

    this._close = this._close.bind(this);
    this._logoutClicked = this._logoutClicked.bind(this);
  }

  _close() {
    this.setState({open: false})
  }

  _changeSubsStatus(name) {
    let actives = this.state.actives.slice();
    if (actives.includes(name)) {
      actives = actives.filter(a => a != name);
    }
    else {
      actives.push(name);
    }
    this.setState({actives})
  }

  _logoutClicked() {
    this.auth.logout();
  }

  render() {
    const {
      open,
      actives
    } = this.state;

    const hamburgerIconClassName = open ? "animated-icon open" : "animated-icon";
    const navOverlayClassName = open ? "nav-overlay open" : "nav-overlay";

    return (
      <>
        <span className="nav-overlay-toggler">
          <button className="navbar-toggler navbar-button" type="button">
            <div onClick={() => this.setState({open: !open})} className={hamburgerIconClassName}><span></span><span></span><span></span><span></span></div>
          </button>
        </span>

        <div className={navOverlayClassName}>
          <ul className="nav-overlay-list">
            <li className="nav-overlay-list-item">
              <Link onClick={this._close} className="nav-overlay-list-item-link" to="/database/monster">Monsters</Link>
            </li>
            <li className="nav-overlay-list-item">
              <Link onClick={this._close} className="nav-overlay-list-item-link" to="/database">Items</Link>
            </li>
            <li className="nav-overlay-list-item">
              <Link onClick={this._close} className="nav-overlay-list-item-link" to="/database/quest">Quests</Link>
            </li>
            <li className="nav-overlay-list-item">
              <Link onClick={() => this._changeSubsStatus("planner")} className="nav-overlay-list-item-link" to="#">Planner</Link>
              {actives.includes("planner") && (
                <ul className="nav-overlay-list-item-subs">
                  <li>
                    <Link onClick={this._close} className="nav-overlay-list-item-sub-link" to="/planner/explorer">Explorer</Link>
                  </li>
                  <li>
                    <Link onClick={this._close} className="nav-overlay-list-item-sub-link" to="/planner/saint">Saint</Link>
                  </li>
                  <li>
                    <Link onClick={this._close} className="nav-overlay-list-item-sub-link" to="/planner/noble">Noble</Link>
                  </li>
                  <li>
                    <Link onClick={this._close} className="nav-overlay-list-item-sub-link" to="/planner/mercenary">Mercenary</Link>
                  </li>
                  <li>
                    <Link onClick={this._close} className="nav-overlay-list-item-sub-link" to="/planner/ship">Ship</Link>
                  </li>
                </ul>
              )}
            </li>

            <li className="nav-overlay-list-item">
              <Link onClick={() => this._changeSubsStatus("social")} className="nav-overlay-list-item-link" to="#">Social</Link>
              {actives.includes("social") && (
                <ul className="nav-overlay-list-item-subs">
                  <li>
                    <a onClick={this._close} className="nav-overlay-list-item-sub-link" target="_blank" href="https://github.com/HealYouDown/flandria">Github</a>
                  </li>
                  <li>
                    <a onClick={this._close} className="nav-overlay-list-item-sub-link" target="_blank" href="https://discord.gg/cg3Zxu2">Discord</a>
                  </li>
                  <li>
                    <a onClick={this._close} className="nav-overlay-list-item-sub-link" target="_blank" href="https://www.patreon.com/flandria">Patreon</a>
                  </li>
                </ul>
              )}
            </li>

            {this.auth.loggedIn()
            ? (
              <li className="nav-overlay-list-item">
                <Link onClick={() => this._changeSubsStatus("account")} className="nav-overlay-list-item-link" to="#">{this.auth.getUsername()}</Link>
                {actives.includes("account") && (
                  <ul className="nav-overlay-list-item-subs">
                    <li>
                      <Link className="nav-overlay-list-item-sub-link" onClick={this._logoutClicked} to="#">Logout</Link>
                    </li>
                    {this.auth.isAdmin() && (
                      <li>
                        <Link onClick={this._close} className="nav-overlay-list-item-sub-link" to="/dashboard">Dashboard</Link>
                      </li>
                    )}
                  </ul>
                )}
              </li>
            )
            : (
              <li className="nav-overlay-list-item">
                <Link onClick={this._close} className="nav-overlay-list-item-link" to="/auth/login">Login</Link>
              </li>
            )
            }

          </ul>
        </div>
      </>
    )
  }
}