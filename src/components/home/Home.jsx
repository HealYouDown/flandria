import React from "react";
import ItemSearch from "../shared/ItemSearch";
import { withRouter } from "react-router-dom";

class Home extends React.Component {
  componentDidMount() {
    document.title = "Home"
  }

  render() {
    return (
      <div style={{display: "flex", justifyContent: "center", alignItems: "center", height: "100%"}}>
        <div style={{marginBottom: "100px", width: "100%"}}>
          <ItemSearch 
            searchInputStyle={{fontSize: "24px"}}
            searchInputWrapperStyle={{padding: "0px 40px"}}
            clickAction={item => this.props.history.push(`/database/${item.table}/${item.code}`)}
          />
        </div>
      </div>
    )
  }
}

export default withRouter(Home);