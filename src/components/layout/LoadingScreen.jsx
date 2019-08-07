import React from "react";
import "./LoadingScreen.css";
import Background from "./Background";

const LoadingScreen = () => {
  return (
    <div className="loading-screen">
      <div className="loading-screen-inner">
        <img src="/static/img/favicon.png" />
        <span className="loading-text loading-dots">Preparing ship to set sail</span>
      </div>

      <Background />
      
    </div>
  )
}

export default LoadingScreen;