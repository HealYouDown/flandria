import { BrowserRouter } from "react-router-dom";
import { ScreenClassProvider } from "react-grid-system";
import React from "react";

import { routes } from "./Routes";
import Layout from "./layout/Layout";
import GaListener from "./GaListener";


export default class App extends React.Component {
  render() {
    return (
      <ScreenClassProvider>
        <BrowserRouter>
          <GaListener trackingId="UA-131501670-1">
            <Layout>
              {routes}
            </Layout>
          </GaListener>
        </BrowserRouter>
      </ScreenClassProvider>
    )
  }
}
