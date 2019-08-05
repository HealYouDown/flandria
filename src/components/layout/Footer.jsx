import React from "react";
import { Link } from "react-router-dom";

export default class Footer extends React.Component {
  render() {
    return (
      <footer>
          <div>
            <Link to="/about">About</Link>
          </div>

          <div>
            © 2019 Copyright:
            <Link to="/"> Flandria.info</Link>
          </div>

          <div>
            <Link to="/privacy-policy">Privacy Policy</Link>
          </div>
        </footer>
    )
  }
}
