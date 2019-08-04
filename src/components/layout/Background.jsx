import React from "react";
import { withRouter } from "react-router-dom";

import "./Background.css"

class Background extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      backgroundImage: this._getBackgroundBasedOnUrl(this.props.history.location.pathname)
    }

    this.props.history.listen((location, action) => {
      this.setState({
        backgroundImage: this._getBackgroundBasedOnUrl(location.pathname)
      })
    })
  }

  _getBackgroundBasedOnUrl(url) {    
    const urlToBg = {
      "/planner/explorer": "/static/img/backgrounds/explorer.jpg",
      "/planner/saint": "/static/img/backgrounds/saint.jpg",
      "/planner/noble": "/static/img/backgrounds/noble.jpg",
      "/planner/mercenary": "/static/img/backgrounds/mercenary.jpg",
      "/planner/ship": "/static/img/backgrounds/ship.jpg",
    }

    return urlToBg[url] || "/static/img/backgrounds/background-image-4.jpeg"
  }

  render() {
    return (
      <>
        <div className="background" style={{ backgroundImage: `url(${this.state.backgroundImage})` }} />
        <div className="background-cover" />
      </>
    )
  }
}

export default withRouter(Background);