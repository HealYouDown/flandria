import Axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import TopBarProgress from 'react-topbar-progress-indicator';
import { AiFillStar, AiOutlineStar } from 'react-icons/ai';
import { HiTrash } from 'react-icons/hi';
import {
  getApiUrl, getImagePath, setWindowTitle, tablenameToTitle,
} from '../../helpers';
import useAsyncError from '../errors/useAsyncError';
import Breadcrumbs from '../shared/Breadcrumbs';
import { isAuthenticated, getIdentity, getToken } from '../auth/auth';
import IconGroup from '../shared/IconGroup';
import { characterClassToIconName } from '../../constants';

const BuildsView = (props) => {
  const { match } = props;
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState(null);
  const throwError = useAsyncError();

  const fetchData = async () => {
    const url = `${getApiUrl()}/planner/${match.params.classname}/builds`;

    try {
      const result = await Axios(url);
      setData(result.data);
      setIsLoading(false);
    } catch (error) {
      throwError(new Error(error));
    }
  };

  useEffect(() => {
    setWindowTitle(`Builds ${tablenameToTitle(match.params.classname)}`);

    setIsLoading(true);
    fetchData();
  }, []);

  const deleteBuild = async (event, buildId) => {
    event.preventDefault();

    // eslint-disable-next-line no-alert, no-restricted-globals
    if (confirm('Really delete the build?')) {
      const url = `${getApiUrl()}/planner/builds/${buildId}/delete`;
      await Axios.delete(url, {
        headers: { Authorization: `Bearer ${getToken()}` },
      });

      setData([...data.filter((build) => build.id !== buildId)]);
    }
  };

  const onStarClick = async (event, buildId, userHasLiked) => {
    event.preventDefault();

    if (isAuthenticated()) {
      let url = '';

      if (userHasLiked) {
        // Delete
        url = `planner/builds/${buildId}/star/delete`;

        await Axios.delete(`${getApiUrl()}/${url}`, {
          headers: { Authorization: `Bearer ${getToken()}` },
        });
      } else {
        // Add
        url = `planner/builds/${buildId}/star/add`;

        await Axios.post(`${getApiUrl()}/${url}`, {}, {
          headers: { Authorization: `Bearer ${getToken()}` },
        });
      }

      // Update data to reflect the new changes
      const buildsWithoutChangedOne = [...data.filter((b) => b.id !== buildId)];
      const changedBuild = data.filter((b) => b.id === buildId)[0];
      console.log(buildsWithoutChangedOne, changedBuild);
      const userId = getIdentity().id;

      if (userHasLiked) {
        changedBuild.stars = changedBuild.stars.filter((star) => star.user_id !== userId);
      } else {
        changedBuild.stars.push({
          id: -1,
          user_id: userId,
          created_at: -1,
        });
      }

      setData([...buildsWithoutChangedOne, changedBuild]);
    }
  };

  return (
    <>
      {isLoading && (<TopBarProgress />)}
      <div className="flex flex-col pb-3 border-b border-gray-200 dark:border-dark-3">
        <div className="flex flex-row items-end justify-between">
          <div>
            <Breadcrumbs
              items={[
                { text: 'Planner', url: '/' },
                { text: tablenameToTitle(match.params.classname), url: `/planner/${match.params.classname}` },
                { text: 'Builds', url: `/planner/${match.params.classname}/builds` },
              ]}
            />
            <h2 className="mt-2 text-2xl font-semibold text-gray-700 md:text-3xl dark:text-white">
              Builds
              {' '}
              {tablenameToTitle(match.params.classname)}
            </h2>
          </div>
        </div>
      </div>
      {(data && data.length > 0 && !isLoading) && (
      <div className="grid grid-cols-1 gap-6 py-3 md:grid-cols-2 lg:grid-cols-3">
          {data.sort((a, b) => b.stars.length > a.stars.length).map((build) => {
            const link = `/planner/${match.params.classname}#${build.build_hash}`;
            let userHasLiked = false;
            let userId = -1;

            if (isAuthenticated()) {
              userId = getIdentity().id;
              build.stars.forEach((star) => {
                if (star.user_id === userId) {
                  userHasLiked = true;
                }
              });
            }

            return (
              <Link
                key={build.id}
                to={link}
                className="flex flex-col rounded-md cursor-pointer bg-gray-50 dark:bg-dark-3 hover:animate-scale"
              >
                <div className="flex justify-between px-4 py-2 bg-gray-200 dark:bg-dark-1 rounded-t-md">
                  <div className="flex items-center space-x-2">
                    <IconGroup
                      icons={[
                        getImagePath(`class_icons/male_${characterClassToIconName[build.character_class.value]}.png`),
                        getImagePath(`class_icons/female_${characterClassToIconName[build.character_class.value]}.png`),
                      ]}
                      space="-space-x-3"
                    />
                    <h3 className="font-semibold text-gray-900 dark:text-white">{build.build_title}</h3>
                  </div>
                  <div className="flex space-x-0.5 items-center">
                    {isAuthenticated() ? (
                      <>
                        <button
                          type="button"
                          onClick={(e) => onStarClick(e, build.id, userHasLiked)}
                          className={`flex gap-x-0.5 items-center transition-colors duration-75 ${userHasLiked ? 'hover:text-red-400 dark:hover:text-red-500 text-blue-500 dark:text-blue-500' : 'hover:text-blue-400 dark:hover:text-blue-500 text-gray-700 dark:text-white'}`}
                        >
                          {userHasLiked ? (
                            <AiFillStar class="w-6 h-6" />
                          ) : (
                            <AiOutlineStar class="w-6 h-6" />
                          )}
                          {build.stars.length}
                        </button>
                        {((userId === build.user.id) || getIdentity().admin) && (
                        <HiTrash
                          onClick={(e) => deleteBuild(e, build.id)}
                          class="w-6 h-6 hover:text-red-500 text-red-400 transition-colors duration-75"
                        />
                        )}
                      </>
                    ) : (
                      <button
                        type="button"
                        className="flex gap-x-0.5 items-center text-gray-700 dark:text-white"
                      >
                        <AiOutlineStar class="w-6 h-6" />
                        {build.stars.length}
                      </button>
                    )}
                  </div>
                </div>
                {build.build_description.length > 0 && (
                <div className="flex-grow px-4 py-2">
                  <p className="text-sm text-gray-700 dark:text-white dark:text-opacity-75">
                    {build.build_description}
                  </p>
                </div>
                )}
                <div className="px-4 py-2 text-sm text-gray-500 dark:text-white dark:text-opacity-50">
                  <span>
                    Posted by
                    {' '}
                    {build.user.username}
                    {' '}
                    on
                    {' '}
                    {new Date(build.created_at).toLocaleDateString()}
                  </span>
                </div>
              </Link>
            );
          })}
      </div>
      )}
      {data && data.length === 0 && (
        <p className="text-lg text-white text-opacity-75">No builds found.</p>
      )}
    </>
  );
};

export default BuildsView;
