import React, { useEffect, useState, useRef } from "react";
import { getMapPoints } from "../fetch";
import TopBarProgress from "react-topbar-progress-indicator";
import styled from "styled-components";
import MonsterShowCheckbox from "./MonsterShowCheckbox";
import breakpoint from "../breakpoint";
import { BLUE } from "../colors";
import history from "../history";
import Ad from "../common/Ad";

var resizedWidth = 512 + 256;
var resizedHeight = 512 + 256;
var dotSize = 4;

if (screen.width <= resizedWidth + 50) {
  resizedWidth = screen.width - 50;
  resizedHeight = screen.width - 50;
  dotSize = 2;
}

const colorsList = [
  "#ff0000",
  "#a60000",
  "#ff5757",
  "#ff6600",
  "#ff954f",
  "#e3a300",
  "#ffcb47",
  "#ffe45e",
  "#eeff00",
  "#bfff00",
  "#84ff00",
  "#03ffc8",
  "#73ffe1",
  "#1fdaff",
  "#0daaff",
  "#7a7aff",
  "#4e4eba",
  "#0d0dd9",
  "#c887fa",
  "#7622b5",
  "#f461ff",
  "#ff17a6",
  "#1b750d",
  "#D4AF37",
  "#71a6d2",
  "#ff003f",
  "#646e00",
  "#00ffc0",
  "#008080",
  "#5f9ea0",
  "#d0db61",
  "#8b4513",
  "#800000",
  "#02075d",
]

const MapWrapper = styled.div`
`

const Button = styled.button`
  border: none;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 5px 15px;
  cursor: pointer;
  transition: color 0.3s;
  border-radius: 3px;
  font-size: 13px;

  margin-left: ${props => props.marginLeft}px;

  &:hover {
    background-color: rgba(0, 0, 0, 0.7);
    color: ${BLUE};
  }
`

const ButtonWrapper = styled.div`
  margin-bottom: 2px;
`

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

  const urlParams = new URLSearchParams(location.search);
  var monsterToShow = null;
  if (urlParams.has("show")) {
    monsterToShow = urlParams.get("show");
    history.replace({
      search: "",
    });
  }

  useEffect(() => {
    getMapPoints(mapCode)
      .then(res => res.json())
      .then(json => {
        setData(json)

        document.title = json.map.name;

        let _cbState = {}
        let _colorState = {}
        Object.keys(json.values).forEach((monsterCode, index) => {
          // checkbox (show) state
          if (monsterToShow === null) {
            _cbState[monsterCode] = true;            
          } else {
            if (monsterToShow == monsterCode) {
              _cbState[monsterCode] = true;            
            } else {
              _cbState[monsterCode] = false;            
            }
          }
          // color
          //_colorState[monsterCode] = colorsList[index];
          _colorState[monsterCode] = "#" + Math.random().toString(16).slice(2, 8); 
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
  
    const left = data.map.left;
    const top = data.map.top;
    const width = data.map.width;
    const height = data.map.height;

    const dots = [];

    Object.keys(checkboxState).forEach(monsterCode => {
      if (checkboxState[monsterCode] === true) {
        ctx2.fillStyle = colorState[monsterCode];

        let points = data.values[monsterCode].points;
        
        const queryParams = new URLSearchParams(location.search);
        const hasDebug = queryParams.has("debug");

        points.forEach(point => {
          let newX = (((point.x - left) / width) * resizedWidth); 
          let newY = (((top - point.y) / height) * resizedHeight);
    
          // ctx2.fillRect(newX - dotSize/2, newY - dotSize/2, dotSize, dotSize);
          ctx2.beginPath();
          ctx2.arc(newX, newY, dotSize, 0, 2*Math.PI, false);
          ctx2.fill()

          let name;
          let monsterName = data.values[monsterCode].monster.name;

          if (hasDebug) {
            name = `${monsterName} (${point.id})`
          } else {
            name = monsterName;
          }

          dots.push({
            x: newX-dotSize,
            y: newY-dotSize,
            width: dotSize*2,
            height: dotSize*2,
            name
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

  const toggleAll = (state) => {
    let s = Object.assign({}, checkboxState);
    Object.keys(s).forEach(key => {
      s[key] = state ? true : false;
    })
    setCheckboxState(s);
  }

  if (loading) {
    return <TopBarProgress />
  }

  return (
    <>
      <Wrapper>
        <MapWrapper>
          <ButtonWrapper>
            <Button onClick={() => toggleAll(true)}>Toggle all: On</Button>
            <Button onClick={() => toggleAll(false)} marginLeft={5}>Toggle all: Off</Button>
          </ButtonWrapper>
          <CanvasWrapper>
            <Canvas ref={mapRef} width={resizedWidth} height={resizedHeight} zIndex={0} />
            <Canvas ref={mapPointsRef} width={resizedWidth} height={resizedHeight} zIndex={100} />
            <TooltipCanvas ref={tooltipRef} />
          </CanvasWrapper>
        </MapWrapper>

        <Grid>
          {Object.keys(data.values).sort((a, b) => data.values[a].monster.level - data.values[b].monster.level).map(monsterCode => {
            const monster = data.values[monsterCode].monster;
            const color = colorState[monsterCode];
            const cbState = checkboxState[monsterCode];
      
            return (
              <MonsterShowCheckbox
                monster={monster}
                onClick={() => onCheckboxChange(monsterCode)}
                active={cbState}
                color={color}
              />
            )
          })}
        </Grid>
      </Wrapper>
      <Ad slot="8700199360" />
    </>
  )
}

export default Maps;