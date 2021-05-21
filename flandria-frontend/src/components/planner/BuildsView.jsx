import Axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import TopBarProgress from 'react-topbar-progress-indicator';
import { AiFillStar, AiOutlineStar } from 'react-icons/ai';
import { getApiUrl, setWindowTitle, tablenameToTitle } from '../../helpers';
import useAsyncError from '../errors/useAsyncError';
import Breadcrumbs from '../shared/Breadcrumbs';
import { isAuthenticated, getIdentity } from '../auth/auth';

const BuildsView = (props) => {
  const { match } = props;
  const [isLoading, setIsLoading] = useState(true);
  const [data, setData] = useState(null);
  const throwError = useAsyncError();

  useEffect(() => {
    setWindowTitle(`Builds ${tablenameToTitle(match.params.classname)}`);

    // Refetch data
    const url = `${getApiUrl()}/planner/${match.params.classname}/builds`;
    const fetchData = async () => {
      try {
        const result = await Axios(url);
        console.log(result.data);
        setData(result.data);
        setIsLoading(false);
      } catch (error) {
        throwError(new Error(error));
      }
    };

    setIsLoading(true);
    fetchData();
  }, []);

  const onStarClick = (event, buildId, userHasLiked) => {
    event.preventDefault();

    if (userHasLiked) {
      // Delete
    } else {
      // Add
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
      {(data && !isLoading) && (
      <div className="grid grid-cols-1 gap-6 py-3 md:grid-cols-2 lg:grid-cols-3">
          {data.map((build) => {
            const link = `/planner/${match.params.classname}#${build.build_hash}`;
            let userHasLiked = false;

            if (isAuthenticated) {
              const userId = getIdentity().id;
              build.stars.forEach((star) => {
                if (star.user_id === userId) {
                  userHasLiked = true;
                }
              });
            }

            return (
              <Link
                to={link}
                className="flex flex-col rounded-md cursor-pointer bg-gray-50 dark:bg-dark-3 hover:animate-scale"
              >
                <div className="flex justify-between px-4 py-2 bg-gray-200 dark:bg-dark-1 rounded-t-md">
                  <h3 className="font-semibold text-gray-900 dark:text-white">{build.build_title}</h3>
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
                </div>
                <div className="flex-grow px-4 py-2">
                  {build.build_description && (
                  <p className="text-sm text-gray-700 dark:text-white dark:text-opacity-75">
                    {build.build_description}
                  </p>
                  )}
                </div>
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
    </>
  );
};

export default BuildsView;
