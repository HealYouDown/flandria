import Axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import TopBarProgress from 'react-topbar-progress-indicator';
import { getApiUrl, setWindowTitle } from '../../helpers';
import InformationWidget from '../database/DetailedTableView/Widgets/InformationWidget';
import ListWidget, { ItemListWidgetItem } from '../database/DetailedTableView/Widgets/ListWidget';
import useAsyncError from '../errors/useAsyncError';
import Breadcrumbs from '../shared/Breadcrumbs';
import Grid, { Column } from '../shared/Grid';

const GuildView = () => {
  const { guildName } = useParams();

  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState(null);

  const throwError = useAsyncError();

  useEffect(() => {
    const url = `${getApiUrl()}/ranking/guilds/${guildName}`;

    const fetchData = async () => {
      try {
        const result = await Axios.get(url);

        setData(result.data);
        setIsLoading(false);

        setWindowTitle(`Guilds - ${result.data.guild.name}`);
      } catch (error) {
        throwError(new Error(error));
      }
    };

    setIsLoading(true);
    fetchData();
  }, [guildName]);

  if (isLoading) return <TopBarProgress />;

  return (
    <>
      <div className="flex items-end justify-between pb-3 border-b border-gray-200 dark:border-dark-3">
        <div>
          <Breadcrumbs
            items={[
              { text: 'Ranking', url: '/' },
              { text: 'Guilds', url: '/ranking/guilds' },
              // use props name parameter as it is encoded (safes encoding it again)
              { text: data.guild.name, url: `/ranking/guilds/${guildName}` },
            ]}
          />
          <div className="flex items-center mt-2">
            <h2 className="mt-0 text-2xl font-semibold text-gray-700 md:text-3xl dark:text-white">
              <span>{data.guild.name}</span>
            </h2>
          </div>
        </div>
      </div>
      <Grid className="mt-3">
        <Column md={4}>
          <InformationWidget tablename="guild" obj={data.guild} />
        </Column>
        <Column md={8}>
          <ListWidget
            label="Members"
          >
            {data.members.sort(
              (a, b) => a.rank > b.rank,
            ).map((member) => (
              <ItemListWidgetItem
                key={member.name}
                tablename="player"
                item={member}
              />
            ))}
          </ListWidget>
        </Column>
      </Grid>
    </>
  );
};

export default GuildView;
