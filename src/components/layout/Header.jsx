import React from "react";
import { Link } from "react-router-dom";
import AuthService from "../AuthService";
import { Hidden, Visible } from "react-grid-system";
import NavOverlay from "./NavOverlay";

export default class Header extends React.Component {
  constructor(props) {
    super(props);

    this.auth = new AuthService();

    this.localStorageUpdated = this.localStorageUpdated.bind(this);
    this.logoutClicked = this.logoutClicked.bind(this);
    this.openDropdown = this.openDropdown.bind(this);
    this.closeDropdown = this.closeDropdown.bind(this);

    this.state = {
      dropdownOpen: false,
      activeDropdown: "",
    }
  }

  componentDidMount() {
    window.addEventListener("storage", this.localStorageUpdated);
  }

  localStorageUpdated() {
    this.forceUpdate();
  }

  logoutClicked() {
    this.closeDropdown();
    this.auth.logout();
  }

  openDropdown(event, activeDropdown) {
    if (!this.state.dropdownOpen) {
      this.setState({
        dropdownOpen: true,
      })

      this.timeout = setTimeout(
        function() {
          this.setState({ activeDropdown });
          this.timeout = null;
        }
        .bind(this),
        300
      );

    }
    else {
      this.setState({ activeDropdown });
    }
  }

  closeDropdown() {
    this.setState({
      dropdownOpen: false,
      activeDropdown: "",
    })

    if (this.timeout) {
      clearTimeout(this.timeout);
      this.timeout = null;
    }
  }

  render() {
    const {
      activeDropdown,
      dropdownOpen,
    } = this.state;

    let dropdownStyle = {}
    if (dropdownOpen) {
      dropdownStyle = {
        height: "200px"
      }
    }

    return (
      <nav>
        <Link to="/">
          <img className="nav-brand" src="/static/img/logo.png" />
        </Link>

        <Hidden xs sm>
          <div className="nav-right">
            <ul className="nav-list">
              <li className="nav-list-item">
                <Link onMouseEnter={this.closeDropdown} className="nav-list-item-link" to="/database/monster">Monsters</Link>
              </li>
              <li className="nav-list-item">
                <Link onMouseEnter={this.closeDropdown} className="nav-list-item-link" to="/database">Items</Link>
              </li>
              <li className="nav-list-item">
                <Link onMouseEnter={this.closeDropdown} className="nav-list-item-link" to="/database/quest">Quests</Link>
              </li>
              <li className="nav-list-item">
                <Link onMouseEnter={e => this.openDropdown(e, "planner")} className="nav-list-item-link" to="#">Planner</Link>
                {activeDropdown == "planner" &&
                  <ul className="nav-list-dropdown">
                    <li>
                      <Link onClick={this.closeDropdown} className="nav-list-item-sub-link" to="/planner/explorer">Explorer</Link>
                    </li>
                    <li>
                      <Link onClick={this.closeDropdown} className="nav-list-item-sub-link" to="/planner/saint">Saint</Link>
                    </li>
                    <li>
                      <Link onClick={this.closeDropdown} className="nav-list-item-sub-link" to="/planner/noble">Noble</Link>
                    </li>
                    <li>
                      <Link onClick={this.closeDropdown} className="nav-list-item-sub-link" to="/planner/mercenary">Mercenary</Link>
                    </li>
                    <li>
                      <Link onClick={this.closeDropdown} className="nav-list-item-sub-link" to="/planner/ship">Ship</Link>
                    </li>
                  </ul>
                }
              </li>
              <li className="nav-list-item">
                <Link onMouseEnter={e => this.openDropdown(e, "social")} className="nav-list-item-link" to="#">Social</Link>
                {activeDropdown == "social" &&
                  <ul className="nav-list-dropdown">
                    <li>
                      <a onClick={this.closeDropdown} className="nav-list-item-sub-link" target="_blank" href="https://github.com/HealYouDown/flandria">Github</a>
                    </li>
                  </ul>
                }
              </li>
              {this.auth.loggedIn()
                ? (
                  <li className="nav-list-item">
                    <Link onMouseEnter={e => this.openDropdown(e, "account")} className="nav-list-item-link" to="#">{this.auth.getUsername()}</Link>
                    {activeDropdown == "account" &&
                      <ul className="nav-list-dropdown">
                        <li>
                          <Link onClick={this.closeDropdown} className="nav-list-item-sub-link" to="/account/builds">Builds</Link>
                        </li>
                        <li>
                          <Link className="nav-list-item-sub-link" onClick={this.logoutClicked} to="#">Logout</Link>
                        </li>
                        {this.auth.isAdmin() &&
                          <li>
                          <Link onClick={this.closeDropdown} className="nav-list-item-sub-link" to="/dashboard">Dashboard</Link>
                          </li>
                        }
                      </ul>
                    }
                  </li>
                )
                : (
                  <li className="nav-list-item">
                    <Link onMouseEnter={this.closeDropdown} className="nav-list-item-link" to="/auth/login">Login</Link>
                  </li>
                )
              }
            </ul>
          </div>

          <div style={dropdownStyle} className="nav-background-dropdown" />
          {dropdownOpen && (
            <div onMouseEnter={this.closeDropdown} className="nav-background-dropdown-reset" />
          )}
        </Hidden>

        <Visible xs sm>
          <NavOverlay />
        </Visible>

      </nav>
    )
  }
}
