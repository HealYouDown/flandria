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
  "/map": "background-image-1.jpeg",
  "/map/AD1_000": "maps/AD1_000.jpeg",
  "/map/AD2_000": "maps/AD2_000.jpeg",
  "/map/AD3_000": "maps/AD3_000.jpeg",
  "/map/AD4_000": "maps/AD4_000.jpeg",
  "/map/AD5_000": "maps/AD5_000.jpeg",
  "/map/AF1_000": "maps/AF1_000.jpeg",
  "/map/AF2_000": "maps/AF2_000.jpeg",
  "/map/AI1_000": "maps/AI1_000.jpeg",
  "/map/AI2_000": "maps/AI2_000.jpeg",
  "/map/AS1_000": "maps/AS1_000.jpeg",
  "/map/BD1_000": "maps/BD1_000.jpeg",
  "/map/BD2_000": "maps/BD2_000.jpeg",
  "/map/BD3_000": "maps/BD3_000.jpeg",
  "/map/BF1_000": "maps/BF1_000.jpeg",
  "/map/BF2_000": "maps/BF2_000.jpeg",
  "/map/BI1_000": "maps/BI1_000.jpeg",
  "/map/BI3_000": "maps/BI3_000.jpeg",
  "/map/CD1_000": "maps/CD1_000.jpeg",
  "/map/CD2_000": "maps/CD2_000.jpeg",
  "/map/CD3_000": "maps/CD3_000.jpeg",
  "/map/CD4_000": "maps/CD4_000.jpeg",
  "/map/CD5_000": "maps/CD5_000.jpeg",
  "/map/CD6_000": "maps/CD6_000.jpeg",
  "/map/CED1_000": "maps/CED1_000.jpeg",
  "/map/CED2_000": "maps/CED2_000.jpeg",
  "/map/CED3_000": "maps/CED3_000.jpeg",
  "/map/CED4_000": "maps/CED4_000.jpeg",
  "/map/CED5_000": "maps/CED5_000.jpeg",
  "/map/CED6_000": "maps/CED6_000.jpeg",
  "/map/CF1_000": "maps/CF1_000.jpeg",
  "/map/CI3_000": "maps/CI3_000.jpeg",
  "/map/CI5_000": "maps/CI5_000.jpeg",
  "/map/DF1_000": "maps/DF1_000.jpeg",
  "/map/ED1_000": "maps/ED1_000.jpeg",
  "/map/ED2_000": "maps/ED2_000.jpeg",
  "/map/EF1_000": "maps/EF1_000.jpeg",
  "/map/EF2_000": "maps/EF2_000.jpeg",
  "/map/EI1_000": "maps/EI1_000.jpeg",
  "/map/EI4_000": "maps/EI4_000.jpeg",
  "/map/SD1F1_000": "maps/SD1F1_000.jpeg",
  "/map/SD1_000": "maps/SD1_000.jpeg",
  "/map/SD2F1_000": "maps/SD2F1_000.jpeg",
  "/map/SD2_000": "maps/SD2_000.jpeg",
  "/map/SR1_000": "maps/SR1_000.jpeg",
  "/map/SR2_000": "maps/SR2_000.jpeg",
  "/map/SR3_000": "maps/SR3_000.jpeg",
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
