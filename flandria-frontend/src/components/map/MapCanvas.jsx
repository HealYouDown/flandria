import React, { useEffect, useRef, useState } from 'react';
import { useDebouncedCallback } from 'use-debounce/lib';
import { getImagePath } from '../../helpers';
import Icon from '../shared/Icon';
import ItemSubs from '../shared/ItemSubs';

const MapCanvas = ({
  mapCode, mapLeft, mapTop, mapWidth, mapHeight, points, colors, className = '', showTooltip = true,
}) => {
  const [hoverPoint, setHoverPoint] = useState(null);
  const mapRef = useRef();
  const drawnPoints = [];

  const drawPoints = (context, clientWidth, clientHeight) => {
    points.forEach((point) => {
      const { x, y } = point.pos;
      const { monster } = point;

      const dotSize = clientWidth / 150;

      // Resizes the absolute map point to relative based on dom element size.
      const relativeX = ((x - mapLeft) / mapWidth) * clientWidth;
      const relativeY = ((mapTop - y) / mapHeight) * clientHeight;

      // Draw dot
      context.fillStyle = colors[monster.code];
      context.beginPath();
      context.arc(relativeX, relativeY, dotSize, 0, 2 * Math.PI, false);
      context.fill();

      // Add point to drawnPoints array to be able to check for hovers
      // later
      drawnPoints.push({
        x: relativeX - dotSize,
        y: relativeY - dotSize,
        width: relativeX + dotSize,
        height: relativeY + dotSize,
        monster,
      });
    });
  };

  const onMouseMove = (event) => {
    // Checks if mouse cursor is hitting any drawn points
    const boundingRect = mapRef.current.getBoundingClientRect();
    const mousePosX = event.clientX - boundingRect.left;
    const mousePosY = event.clientY - boundingRect.top;

    drawnPoints.some((point) => {
      // Check if mouse is in bounding rect of dot
      if (mousePosX >= point.x && mousePosX <= point.width
            && mousePosY >= point.y && mousePosY <= point.height) {
        setHoverPoint(point);
        return true;
      }
      setHoverPoint(null);
      return false;
    });
  };

  const updateCanvas = () => {
    if (!mapRef.current) return;
    const { clientWidth } = mapRef.current;
    // Clear drawn points array
    drawnPoints.length = 0;

    // Update canvas internal size with dom size so images
    // are not stretched etc.
    mapRef.current.width = clientWidth;
    mapRef.current.height = clientWidth;

    const context = mapRef.current.getContext('2d');
    context.clearRect(0, 0, clientWidth, clientWidth);

    drawPoints(context, clientWidth, clientWidth);

    mapRef.current.onmousemove = onMouseMove;
  };

  useEffect(() => {
    updateCanvas();
  }, [mapCode, points]);

  const debouncedUpdateCanvas = useDebouncedCallback(() => {
    updateCanvas();
  }, 500);

  useEffect(() => {
    // Updates canvas 500ms after resizing
    window.addEventListener('resize', debouncedUpdateCanvas.callback);
    return () => window.removeEventListener('resize', debouncedUpdateCanvas.callback);
  }, []);

  return (
    <>
      <canvas
        className={`w-full h-full bg-cover ${className}`}
        style={{ backgroundImage: `url(${getImagePath(`maps/${mapCode}.png`)})` }}
        ref={mapRef}
      />
      {(hoverPoint && showTooltip) && (
      <div
        className="absolute z-10 flex items-center px-1.5 py-1 text-gray-700 bg-white rounded-sm shadow-md dark:bg-dark-3 dark:text-white"
        style={{
          top: mapRef.current.offsetTop + hoverPoint.y - 10,
          left: mapRef.current.offsetLeft + hoverPoint.x + 25,
        }}
      >
        <Icon
          tablename="monster"
          icon={hoverPoint.monster.icon}
          rareGrade={hoverPoint.monster.rating.value}
          className="w-8 h-8 mr-1 border-opacity-100"
        />
        <div className="flex flex-col">
          <span>{hoverPoint.monster.name}</span>
          <ItemSubs tablename="monster" item={hoverPoint.monster} />
        </div>
      </div>
      )}
    </>
  );
};

export default MapCanvas;
