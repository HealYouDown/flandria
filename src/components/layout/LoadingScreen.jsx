import React from "react";
import TopBarProgress from "react-topbar-progress-indicator"
 
TopBarProgress.config({
  barColors: {
    "0": "#5695d4",
    "1.0": "#5695d4",
  },
  shadowBlur: 5,
})

const LoadingScreen = () => {
  return <TopBarProgress />
}

export default LoadingScreen;