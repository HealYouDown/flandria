import React, { useState } from "react";
import history from "../history";
import styled from "styled-components";

const ImageBackgroundCover = styled.div`
  position: fixed;
  background: rgba(0, 0, 0, 0.8);
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
`

const ImageBackground = styled.div`
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  z-index: -1;
  background-image: url("/static/assets/backgrounds/${props => props.image}");
`

const pathnameToImage = {
  "/planner/explorer": "explorer.jpg",
  "/planner/saint": "saint.jpg",
  "/planner/noble": "noble.jpg",
  "/planner/mercenary": "mercenary.jpg",
  "/planner/ship": "ship.jpg",
  // Maps
  "/map/AF2_000": "splash_images/wide_af2_Jp.png",
}

const defaultBackgroundImage = "background-image-2.jpeg";

/**
 * Background Component that listens to active url and applies
 * a new background image based on the url. 
 */
const Background = () => {
  const [pathname, setPathname] = useState(location.pathname);

  history.listen((location, action) => {
    setPathname(location.pathname);
  })

  const backgroundImage = pathnameToImage[pathname] || defaultBackgroundImage;

  return (
    <>
      <ImageBackground image={backgroundImage} />
      <ImageBackgroundCover />
    </>
  )
}

export default Background;
