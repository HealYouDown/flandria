/* eslint-disable camelcase */
import Axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import TopBarProgress from 'react-topbar-progress-indicator';
import { characterClassToIconName } from '../../constants';
import { getApiUrl, getImagePath, setWindowTitle } from '../../helpers';
import InformationWidget from '../database/DetailedTableView/Widgets/InformationWidget';
import ListWidget, { TextListWidgetItem } from '../database/DetailedTableView/Widgets/ListWidget';
import useAsyncError from '../errors/useAsyncError';
import Breadcrumbs from '../shared/Breadcrumbs';
import Grid, { Column } from '../shared/Grid';
import IconGroup from '../shared/IconGroup';

const PlayerHistoryItem = ({ historyObj }) => {
  const dateString = new Date(historyObj.inserted_at).toLocaleDateString();
  const changes = [];

  const changeKeys = Object.keys(historyObj.changes);

  if (changeKeys.includes('previous_level_land')) {
    changes.push(
      `Land level: ${historyObj.changes.previous_level_land} -> ${historyObj.changes.new_level_land}`,
    );
  }

  if (changeKeys.includes('previous_level_sea')) {
    changes.push(
      `Sea level: ${historyObj.changes.previous_level_sea} -> ${historyObj.changes.new_level_sea}`,
    );
  }

  if (changeKeys.includes('previous_character_class')) {
    changes.push(
      `Class: ${historyObj.changes.previous_character_class.name} -> ${historyObj.changes.new_character_class.name}`,
    );
  }

  if (changeKeys.includes('previous_guild')) {
    const { previous_guild, new_guild } = historyObj.changes;
    if (!previous_guild && new_guild) {
      changes.push(`Joined ${new_guild}`);
    } else if (previous_guild && !new_guild) {
      changes.push(`Left ${previous_guild}`);
    } else {
      changes.push(`Changed guild from ${previous_guild} to ${new_guild}`);
    }
  }

  return (
    <TextListWidgetItem>
      <b>{dateString}</b>
      {changes.map((changeString) => <span key={changeString} className="block">{changeString}</span>)}
    </TextListWidgetItem>
  );
};

const PlayerView = () => {
  const { server, name } = useParams();

  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState(null);

  const throwError = useAsyncError();

  useEffect(() => {
    const url = `${getApiUrl()}/ranking/players/${server}/${name}`;

    const fetchData = async () => {
      try {
        const result = await Axios.get(url);

        setData(result.data);
        setIsLoading(false);

        setWindowTitle(`Player - ${result.data.name}`);
      } catch (error) {
        throwError(new Error(error));
      }
    };

    setIsLoading(true);
    fetchData();
  }, [server, name]);

  if (isLoading) return <TopBarProgress />;

  return (
    <>
      <div className="flex items-end justify-between pb-3 border-b border-gray-200 dark:border-dark-3">
        <div>
          <Breadcrumbs
            items={[
              { text: 'Ranking', url: '/' },
              { text: name, url: `/ranking/players/${server}/${name}` },
            ]}
          />
          <div className="flex items-center mt-2">
            <IconGroup
              space="-space-x-5"
              size="w-10 h-10"
              icons={[
                getImagePath(`class_icons/female_${characterClassToIconName[data.character_class.value]}.png`),
                getImagePath(`class_icons/male_${characterClassToIconName[data.character_class.value]}.png`),
              ]}
            />
            <h2 className="ml-1.5 mt-0 text-2xl font-semibold text-gray-700 md:text-3xl dark:text-white">
              <span>{data.name}</span>
            </h2>
          </div>
        </div>
      </div>
      <Grid className="mt-3">
        <Column md={4}>
          <InformationWidget tablename="player" obj={data} />
        </Column>
        <Column md={8}>
          <ListWidget
            label="History"
          >
            {data.history.map((historyObj) => (
              <PlayerHistoryItem key={historyObj.inserted_at} historyObj={historyObj} />
            ))}
            {data.history.length === 0 && (
            <TextListWidgetItem>
              No history available.
            </TextListWidgetItem>
            )}
          </ListWidget>
        </Column>
      </Grid>
    </>
  );
};

export default PlayerView;
