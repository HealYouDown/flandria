import React from 'react';
import Card, { CardHeader, CardHeaderTitle } from '../../../shared/Card';
import MapCanvas from '../../../map/MapCanvas';

const MonsterMapsWidget = ({ monster, mapPoints }) => {
  if (mapPoints.length === 0) return null;

  const groupedPoints = {};
  mapPoints.forEach((point) => {
    const objToPush = {
      pos: point.pos,
      monster,
    };
    if (point.map.code in groupedPoints) {
      groupedPoints[point.map.code].points.push(objToPush);
    } else {
      groupedPoints[point.map.code] = {
        map: point.map,
        points: [objToPush],
      };
    }
  });

  return (
    <>
      {Object.keys(groupedPoints).map((mapCode) => {
        const { map, points } = groupedPoints[mapCode];
        return (
          <Card
            key={mapCode}
            header={(
              <CardHeader>
                <CardHeaderTitle>{map.name}</CardHeaderTitle>
              </CardHeader>
            )}
          >
            <MapCanvas
              colors={{ [monster.code]: 'red' }}
              mapLeft={map.left}
              mapTop={map.top}
              mapWidth={map.width}
              mapHeight={map.height}
              mapCode={map.code}
              points={points}
              className="rounded-b-md"
            />
          </Card>
        );
      })}
    </>
  );
};

export default MonsterMapsWidget;
