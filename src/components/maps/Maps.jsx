import React, { useEffect, useState, useRef } from "react";
import { getMapPoints } from "../fetch";
import TopBarProgress from "react-topbar-progress-indicator";
import styled from "styled-components";
import MonsterShowCheckbox from "./MonsterShowCheckbox";
import breakpoint from "../breakpoint";

const resizedWidth = 512 + 128;
const resizedHeight = 512 + 128;
const dotSize = 4;


const Grid = styled.div`
  display: grid;
  grid-column-gap: 30px;
  grid-row-gap: 20px;
  padding: 0px 0px;
  width: 100%;

  ${breakpoint("sm")`
    grid-template-columns: 1fr;
  `}
  ${breakpoint("md")`
    grid-template-columns: 1fr 1fr;
    `}
  ${breakpoint("lg")`
    grid-template-columns: 1fr 1fr 1fr;
  `}
  ${breakpoint("xl")`
    grid-template-columns: 1fr 1fr 1fr 1fr;
  `}
`

const CanvasWrapper = styled.div`
  position: relative;
  height: ${resizedHeight}px;
  width: ${resizedWidth}px;
  margin-bottom: 20px;
`

const Wrapper = styled.div`
  display: flex;
  flex-flow: column;
  align-items: center;
`

const Canvas = styled.canvas`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: ${props => props.zIndex};
`

const TooltipCanvas = styled.canvas`
  position: absolute;
  z-index: 200;
`

const Maps = (props) => {
  const mapCode = props.match.params.mapCode;
  const [data, setData] = useState();
  const [checkboxState, setCheckboxState] = useState();
  const [colorState, setColorState] = useState();
  const [loading, setLoading] = useState(true);

  const mapRef = useRef(null);
  const mapPointsRef = useRef(null);
  const tooltipRef = useRef(null);

  useEffect(() => {
    getMapPoints(mapCode)
      .then(res => res.json())
      .then(json => {
        setData(json)

        let _cbState = {}
        let _colorState = {}
        Object.keys(json.values).forEach(monsterCode => {
          // ch 
          _cbState[monsterCode] = true;
          // color
          _colorState[monsterCode] = '#' + Math.random().toString(16).substr(2, 6);
        })
        setCheckboxState(_cbState);
        setColorState(_colorState);
    
        setLoading(false);
      });
  }, [])

  useEffect(() => {
    if (loading || checkboxState === undefined) {
      return;
    } 

    /* Canvas 1
    Background Image of the Map
    */
    const ctx1 = mapRef.current.getContext("2d");
    let img = new Image;
    img.onload = () => {
      ctx1.drawImage(img, 0, 0, resizedWidth, resizedHeight);
    }
    img.src = window.location.origin + "/static/assets/maps/" + mapCode + ".png";


    /* Canvas 2
    Dots for each monster
    */
    const ctx2 = mapPointsRef.current.getContext("2d");
    ctx2.clearRect(0, 0, resizedWidth, resizedHeight);

    const left = -63875.937;
    const top = 62559.402;
    const width = 110000;
    const height = 110000;

    const dots = [];

    Object.keys(checkboxState).forEach(monsterCode => {
      if (checkboxState[monsterCode] === true) {
        ctx2.fillStyle = colorState[monsterCode];

        let points = data.values[monsterCode].points;
        points.forEach(point => {
          let newX = (((point["x"] - left) / width) * resizedWidth) - dotSize/2; 
          let newY = (((top - point["y"]) / height) * resizedHeight) - dotSize/2;
    
          // ctx2.fillRect(newX - dotSize/2, newY - dotSize/2, dotSize, dotSize);
          ctx2.beginPath();
          ctx2.arc(newX, newY, dotSize, 0, 2*Math.PI, false);
          ctx2.fill()

          dots.push({
            "x": newX-dotSize,
            "y": newY-dotSize,
            "width": dotSize*2,
            "height": dotSize*2,
            "name": data.values[monsterCode].monster.name,
          });
        })
      }
    })


    // Bind ctx2 mouse hover
    mapPointsRef.current.onmousemove = (e) => {
      const boundingRect = mapPointsRef.current.getBoundingClientRect();
      
      const mousePosX = e.clientX - boundingRect.left;
      const mousePosY = e.clientY - boundingRect.top;

      // using some to break the loop as soon as some rect matches
      let hit = false;
      dots.some(dot => {
        if (mousePosX >= dot.x && mousePosX <= dot.x + dot.width &&
          mousePosY >= dot.y && mousePosY <= dot.y + dot.height) {
            hit = true;
            
            const tooltipCtx = tooltipRef.current.getContext("2d");

            let metrics = tooltipCtx.measureText(dot.name);

            tooltipRef.current.width = metrics.width;
            tooltipRef.current.height = 14;

            tooltipRef.current.style.left = `${dot.x + 20}px`;
            tooltipRef.current.style.top = `${dot.y + 5}px`;
            
            tooltipCtx.clearRect(0, 0, tooltipRef.current.width, tooltipRef.current.height);
            // background color
            tooltipCtx.fillStyle = "#FFFFFF";
            tooltipCtx.fillRect(0, 0, tooltipRef.current.width, tooltipRef.current.height);
            // text
            tooltipCtx.fillStyle = "#000000";
            tooltipCtx.fillText(dot.name, 0, 10);
            return false;
          }
      })
      if (!hit) {
        tooltipRef.current.style.top = "-5000px";
      }
    }

  }, [loading, checkboxState])

  const onCheckboxChange = (monsterCode) => {
    setCheckboxState({...checkboxState, [monsterCode]: !checkboxState[monsterCode]})
  }

  if (loading) {
    return <TopBarProgress />
  }

  return (
    <Wrapper>
      <CanvasWrapper>
        <Canvas ref={mapRef} width={resizedWidth} height={resizedHeight} zIndex={0} />
        <Canvas ref={mapPointsRef} width={resizedWidth} height={resizedHeight} zIndex={100} />
        <TooltipCanvas ref={tooltipRef} />
      </CanvasWrapper>

      <Grid>
        {Object.keys(data.values).sort((a, b) => data.values[a].monster.level - data.values[b].monster.level).map(monsterCode => {
          const monster = data.values[monsterCode].monster;
          const color = colorState[monsterCode];
          const cbState = checkboxState[monsterCode];
    
          return (
            <MonsterShowCheckbox
              monster={monster}
              onChange={() => onCheckboxChange(monsterCode)}
              active={cbState}
              color={color}
            />
          )
        })}
      </Grid>
    </Wrapper>
  )
}

export default Maps;