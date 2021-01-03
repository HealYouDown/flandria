import Axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import TopBarProgress from 'react-topbar-progress-indicator';
import { getApiUrl, setWindowTitle, tablenameToTitle } from '../../helpers';
import useAsyncError from '../errors/useAsyncError';
import Breadcrumbs from '../shared/Breadcrumbs';
import Hash from './Hash';
import SkillTree from './SkillTree';
import StatusPlanner from './StatusPlanner';

const PlannerView = () => {
  const { classname } = useParams();
  const [isLoading, setIsLoading] = useState(true);
  const [fetchResult, setFetchResult] = useState(null);
  const throwError = useAsyncError();
  const [hash, setHash] = useState(null);

  useEffect(() => {
    const url = `${getApiUrl()}/planner/${classname}`;

    const fetchData = async () => {
      try {
        // Fetch result
        const result = await Axios.get(url);

        // Create and load hash
        const hashInstance = new Hash(
          classname,
          Object.keys(result.data.skills),
        );
        if (!hashInstance.exists()) {
          hashInstance.setDefaultHash();
        }
        setHash(hashInstance);

        // Set result after setting hash
        setFetchResult({
          classname,
          data: result.data,
        });
        setIsLoading(false);
      } catch (error) {
        throwError(new Error(error));
      }
    };

    setWindowTitle(tablenameToTitle(classname));
    setIsLoading(true);
    fetchData();
  }, [classname]);

  if (isLoading || fetchResult.classname !== classname) return <TopBarProgress />;

  return (
    <>
      <div className="flex flex-col pb-3 border-b border-gray-200 dark:border-dark-3">
        <div>
          <Breadcrumbs
            items={[
              { text: 'Planner', url: '/' },
              { text: tablenameToTitle(classname), url: `/planner/${classname}` },
            ]}
          />
          <div className="flex items-center mt-2">
            <h2 className="mt-0 text-2xl font-semibold text-gray-700 md:text-3xl dark:text-white">
              {tablenameToTitle(classname)}
            </h2>
          </div>
        </div>
      </div>
      <div className="flex flex-col justify-around mt-3 lg:flex-row gap-y-4 md:gap-y-0">
        <SkillTree
          classname={classname}
          skillData={fetchResult.data.skills}
          hash={hash}
        />
        {classname !== 'ship' && (
        <StatusPlanner
          classname={classname}
          statusData={fetchResult.data.status}
          hash={hash}
        />
        )}
      </div>
    </>
  );
};
export default PlannerView;
