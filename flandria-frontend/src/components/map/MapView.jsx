import Axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import TopBarProgress from 'react-topbar-progress-indicator';
import { getApiUrl, setWindowTitle } from '../../helpers';
import Breadcrumbs from '../shared/Breadcrumbs';
import Grid, { Column } from '../shared/Grid';
import Icon from '../shared/Icon';
import ItemSubs from '../shared/ItemSubs';
import MapCanvas from './MapCanvas';

const ToggleMonsterButton = ({
  monster, onToggleActive, onToggleDeactive, isActive,
}) => (
  <button
    type="button"
    onClick={() => {
      if (isActive) {
        onToggleDeactive(monster);
      } else {
        onToggleActive(monster);
      }
    }}
    className={`flex px-4 py-2 text-gray-700 rounded-lg cursor-pointer dark:text-white outline-none box-border border-2 border-white dark:border-dark-4
              ${isActive ? 'bg-white dark:bg-dark-4 shadow-sm' : ''}`}
  >
    <Icon
      tablename="monster"
      rareGrade={monster.rating.value}
      className="w-10 h-10 mr-1.5 border-opacity-100"
      icon={monster.icon}
    />
    <div className="flex flex-col items-start justify-center">
      <span className="leading-none text-left">{monster.name}</span>
      <ItemSubs tablename="monster" item={monster} />
    </div>
  </button>
);

const MapView = () => {
  const { mapCode } = useParams();
  const [fetchResult, setFetchResult] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedMonsters, setSeletectedMonsters] = useState([]);
  const [colors, setColors] = useState({});

  const getMonstersFromPoints = (points) => {
    const uniqueMonsterObjects = [];
    points.forEach((point) => {
      if (!(uniqueMonsterObjects.some((monster) => monster.code === point.monster.code))) {
        uniqueMonsterObjects.push(point.monster);
      }
    });
    return uniqueMonsterObjects;
  };

  const toggleAll = (bool) => {
    if (bool) {
      // Toggle all on
      setSeletectedMonsters(Object.keys(colors));
    } else {
      // Toggle all off
      setSeletectedMonsters([]);
    }
  };

  useEffect(() => {
    const url = `${getApiUrl()}/database/map/${mapCode}`;
    const fetchData = async () => {
      const result = await Axios.get(url);

      setFetchResult({
        mapCode,
        data: result.data,
      });
      setIsLoading(false);

      // Update window title
      setWindowTitle(result.data.name);

      // Create colors for all monsters in points
      const colorsScoped = {};
      getMonstersFromPoints(result.data.points).forEach((monster) => {
        colorsScoped[monster.code] = `#${Math.random().toString(16).slice(2, 8)}`;
      });
      setColors(colorsScoped);

      // Enable all monsters on first load (colors contains all monster keys :p)
      setSeletectedMonsters(Object.keys(colorsScoped));
    };

    setIsLoading(true);
    fetchData();
  }, [mapCode]);

  if (isLoading) return <TopBarProgress />;

  const { data } = fetchResult;

  return (
    <div>
      <div className="flex flex-col pb-3 border-b border-gray-200 dark:border-dark-3">
        <div>
          <Breadcrumbs
            items={[
              { text: 'Maps', url: '/map' },
              { text: data.name, url: `/map/${mapCode}` },
            ]}
          />
          <div className="flex items-center mt-2">
            <h2 className="mt-0 text-2xl font-semibold text-gray-700 md:text-3xl dark:text-white">
              {data.name}
            </h2>
          </div>
        </div>
      </div>
      <div className="flex flex-col items-center mt-3">
        <div className="flex flex-row gap-5 text-gray-700 dark:text-white">
          <button type="button" onClick={() => toggleAll(true)}>All On</button>
          <button type="button" onClick={() => toggleAll(false)}>All Off</button>
        </div>
        <div
          className="w-full h-full"
          style={{ maxHeight: '768px', maxWidth: '768px' }}
        >
          <MapCanvas
            className="rounded-lg"
            colors={colors}
            mapLeft={data.left}
            mapTop={data.top}
            mapWidth={data.width}
            mapHeight={data.height}
            mapCode={mapCode}
            points={data.points.filter((point) => selectedMonsters.includes(point.monster.code))}
          />
        </div>
        <Grid className="mt-4" gap="gap-4">
          {getMonstersFromPoints(data.points).map((monster) => (
            <Column sm={12} md={6} lg={4} xl={3} gap="gap-4" key={monster.code}>
              <ToggleMonsterButton
                monster={monster}
                isActive={selectedMonsters.includes(monster.code)}
                onToggleActive={(monster_) => setSeletectedMonsters(
                  [...selectedMonsters, monster_.code],
                )}
                onToggleDeactive={(monster_) => setSeletectedMonsters(
                  selectedMonsters.filter((monsterCode) => monsterCode !== monster_.code),
                )}
              />
            </Column>
          ))}
        </Grid>
      </div>
    </div>

  );
};

export default MapView;
