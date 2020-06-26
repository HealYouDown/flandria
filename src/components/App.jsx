import React from "react";
import { Route, Router, Switch } from "react-router-dom";
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import TopBarProgress from "react-topbar-progress-indicator";
import { createGlobalStyle } from "styled-components";
import Login from "./auth/Login";
import Register from "./auth/Register";
import { BLUE } from "./colors";
import DetailedView from "./database/DetailedView";
import Overview from "./database/Overview";
import MonsterEdit from "./database/pages/MonsterEdit";
import TableOverview from "./database/TableOverview";
import history from "./history";
import About from "./home/About";
import Main from "./home/Main";
import PrivacyPolicy from "./home/PrivacyPolicy";
import Layout from "./layout/Layout";
import Planner from "./planner/Planner";
import { ScreenClassProvider } from "react-grid-system";
import GAListener from "./GAListener";
import Builds from "./planner/Builds";
import MapOverview from "./maps/MapOverview";
import Maps from "./maps/Maps";
import RankingOverview from "./ranking/RankingOverview";
import RankingDetailedView from "./ranking/RankingDetailedView";
import EssencePDF from "./home/EssencePDF";

// Global style
const GlobalStyle = createGlobalStyle`
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: black;
}

#react-root-div {
  display: flex;
  flex-flow: column;
  height: 100% !important;
}

main {
  flex-grow: 1;
}

main * {
  color: #aaa;
}

`

// Loadingbar Config
TopBarProgress.config({
  barColors: {
    "0": BLUE,
    "1.0": BLUE,
  },
  shadowBlur: 5
});

const App = () => {
  return (
    <ScreenClassProvider>
      <Router history={history}>
        <GAListener trackingId="UA-131501670-1">
          <Layout>
            <Switch>
              <Route exact path="/" component={Main} />
              <Route exact path="/about" component={About} />
              <Route exact path="/privacy" component={PrivacyPolicy} />
              <Route exact path="/essence-pdf/:lang" component={EssencePDF} />

              <Route exact path="/database" component={TableOverview} />
              <Route exact path="/database/:tablename" component={Overview} />
              <Route exact path="/database/:tablename/:code" component={DetailedView} />
              <Route exact path="/database/monster/:code/edit" component={MonsterEdit} />

              <Route exact path="/ranking/guild" component={RankingOverview} />
              <Route exact path="/ranking/guild/:hash" component={RankingDetailedView} />

              <Route exact path="/planner/:plannerClass" component={Planner} />
              <Route exact path="/planner/:plannerClass/builds" component={Builds} />

              <Route exact path="/map" component={MapOverview} />
              <Route exact path="/map/:mapCode" component={Maps} />

              <Route exact path="/auth/register" component={Register} />
              <Route exact path="/auth/login" component={Login} />
            </Switch>
          </Layout>
        </GAListener>
        <ToastContainer
          autoClose={5000}
          hideProgressBar={false}
          closeOnClick={true}
          pauseOnHover={false}
        />
        <GlobalStyle />
      </Router>
    </ScreenClassProvider>
  )
}

export default App;
