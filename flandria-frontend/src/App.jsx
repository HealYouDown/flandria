import React from 'react';
import {
  BrowserRouter as Router, Route, Switch,
} from 'react-router-dom';
import TopBarProgress from 'react-topbar-progress-indicator';
import { ErrorBoundary } from 'react-error-boundary';
import { CookiesProvider } from 'react-cookie';
import LoginView from './components/auth/LoginView';
import LogoutView from './components/auth/LogoutView';
import RegisterView from './components/auth/RegisterView';
import DetailedTableView from './components/database/DetailedTableView/DetailedTableView';
import ItemsOverview from './components/database/ItemsOverview';
import TableView from './components/database/TableView/TableView';
import Error404Page from './components/errors/404';
import About from './components/home/About';
import LandingPage from './components/home/LandingPage';
import LegalNotice from './components/home/LegalNotice';
import PrivacyPolicy from './components/home/PrivacyPolicy';
import Layout from './components/layout/Layout';
import MapsOverview from './components/map/MapsOverview';
import MapView from './components/map/MapView';
import PlannerView from './components/planner/PlannerView';
import GATracker from './GATracker';
import ErrorBoundaryView from './components/errors/ErrorBoundaryView';
import RankingStatistics from './components/ranking/Statistics';
import GuildOverview from './components/ranking/GuildOverview';
import GuildView from './components/ranking/GuildView';
import PlayerView from './components/ranking/PlayerView';
import PublishBuildView from './components/planner/PublishBuildView';

TopBarProgress.config({
  barColors: {
    '0.0': 'teal',
    '1.0': 'teal',
  },
  shadowBlur: 5,
});

const App = () => (
  <Router>
    <ErrorBoundary
      FallbackComponent={ErrorBoundaryView}
    >
      <GATracker trackingId="UA-131501670-1">
        <CookiesProvider>
          <Layout>
            <Switch>
              <Route path="/" exact component={LandingPage} />
              <Route path="/about" exact component={About} />
              <Route path="/privacy-policy" exact component={PrivacyPolicy} />
              <Route path="/legal-notice" exact component={LegalNotice} />

              <Route path="/auth/login" exact component={LoginView} />
              <Route path="/auth/register" exact component={RegisterView} />
              <Route path="/auth/logout" exact component={LogoutView} />

              <Route path="/database" exact component={ItemsOverview} />
              <Route path="/database/:tablename" exact component={TableView} />
              <Route path="/database/:tablename/:code" exact component={DetailedTableView} />

              <Route path="/map" exact component={MapsOverview} />
              <Route path="/map/:mapCode" exact component={MapView} />

              <Route path="/planner/:classname" exact component={PlannerView} />
              <Route path="/planner/builds/add" exact component={PublishBuildView} />

              <Route path="/ranking/statistics" exact component={RankingStatistics} />
              <Route path="/ranking/guilds" exact component={GuildOverview} />
              <Route path="/ranking/guilds/:guildName" exact component={GuildView} />
              <Route path="/ranking/players/:server/:name" exact component={PlayerView} />

              <Route component={Error404Page} />
            </Switch>
          </Layout>
        </CookiesProvider>
      </GATracker>
    </ErrorBoundary>
  </Router>
);

export default App;
