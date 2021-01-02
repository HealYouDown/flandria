import { Transition } from '@headlessui/react';
import React, { useEffect, useState } from 'react';
import { useHistory, useLocation, useParams } from 'react-router-dom';
import Axios from 'axios';
import TopBarProgress from 'react-topbar-progress-indicator';
import Breadcrumbs from '../../shared/Breadcrumbs';
import FilterMenu from './FilterMenu';
import useDidMountEffect from '../../../useDidMountEffect';
import TableViewItem from './TableViewItem';
import { getApiUrl, setWindowTitle, tablenameToTitle } from '../../../helpers';
import Pagination from '../../shared/Pagination';
import useAsyncError from '../../errors/useAsyncError';

function getQueryParameterOrDefault(key, defaultValue) {
  const params = new URLSearchParams(window.location.search);
  return params.get(key) || defaultValue;
}

function getDefaultFilter(tablename, search) {
  const initialOrderDesc = ['dress', 'hat', 'accessory', 'recipe', 'material', 'random_box', 'consumable'];

  const filter = {
    page: parseInt(getQueryParameterOrDefault('page', 1), 10),
    sort: getQueryParameterOrDefault('sort', 'index'),
    filter: getQueryParameterOrDefault('filter', 'all'),
    area: getQueryParameterOrDefault('area', '-1'),
    effects: getQueryParameterOrDefault('effects', '[]'),
  };

  if (search) {
    // There are some search parameters, that means it is no longer
    // the inital order state, but rather the one given, if any.
    filter.order = getQueryParameterOrDefault('order', 'asc');
  } else {
    filter.order = initialOrderDesc.includes(tablename) ? 'desc' : 'asc';
  }

  return filter;
}

const TableView = () => {
  const { tablename } = useParams();
  const history = useHistory();
  const location = useLocation();
  const throwError = useAsyncError();

  const [filterMenuOpen, setFilterMenuOpen] = useState(false);
  const [filter, setFilter] = useState(getDefaultFilter(tablename, location.search));
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const getUrlWithParameters = () => {
    const searchParams = new URLSearchParams(filter).toString();
    return `${getApiUrl()}/database/${tablename}?${searchParams}`;
  };

  useEffect(() => {
    if (location.state && location.state.filtersChanged) {
      // Update window title
      setWindowTitle(tablenameToTitle(tablename));

      // Refetch data
      const url = getUrlWithParameters();
      const fetchData = async () => {
        try {
          const result = await Axios(url);
          setData({
            url,
            data: result.data,
          });
          setIsLoading(false);
        } catch (error) {
          throwError(new Error(error));
        }
      };

      setIsLoading(true);
      fetchData();
    } else {
      // Table changed; Reset filters. As location changes,
      // this function is called again but this time the
      // if block is excuted.
      setFilter(getDefaultFilter(tablename, ''));
    }
  }, [location]);

  useDidMountEffect(() => {
    // Runs only once the initial render has happened.
    const params = new URLSearchParams(filter);

    const args = {
      pathname: location.pathname,
      search: `?${params.toString()}`,
      state: {
        filtersChanged: true,
      },
    };

    if (!location.search) {
      history.replace(args);
    } else {
      history.push(args);
    }
  }, [filter]);

  return (
    <>
      {isLoading && (<TopBarProgress />)}
      <div className="flex flex-col pb-3 border-b border-gray-200 dark:border-dark-3">
        <div className="flex flex-row items-end justify-between">
          <div>
            <Breadcrumbs
              items={[
                { text: 'Items', url: '/database' },
                { text: tablenameToTitle(tablename), url: `/database/${tablename}` },
              ]}
            />
            <h2 className="mt-2 text-2xl font-semibold text-gray-700 md:text-3xl dark:text-white">{tablenameToTitle(tablename)}</h2>
          </div>
          <button
            type="button"
            onClick={() => setFilterMenuOpen(!filterMenuOpen)}
            className="flex items-center gap-2 px-2 py-1 font-bold text-center text-gray-700 uppercase bg-transparent rounded-lg md:text-lg md:px-6 md:py-2 focus:outline-none hover:bg-gray-200 dark:text-white dark:hover:bg-dark-3"
          >
            Filter
            <svg className="h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
            </svg>
          </button>
        </div>
        <Transition
          show={filterMenuOpen}
        >
          <FilterMenu
            tablename={tablename}
            filter={filter}
            setFilter={setFilter}
          />
        </Transition>
      </div>
      {(data && !isLoading && (data.url === getUrlWithParameters())) && (
        <>
          <div className="grid grid-cols-1 gap-3 py-3 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {data.data.items.map((item) => (
              <TableViewItem
                key={item.code}
                tablename={tablename}
                item={item}
              />
            ))}
          </div>
          <div className="flex flex-row justify-center pt-4">
            <Pagination
              currentPage={filter.page}
              hasPrevious={data.data.pagination.has_previous}
              hasNext={data.data.pagination.has_next}
              labels={data.data.pagination.labels}
              onPageChange={(newPage) => {
                const newFilter = { ...filter };
                newFilter.page = newPage;
                setFilter(newFilter);
              }}
            />
          </div>
        </>
      )}
    </>
  );
};

export default TableView;
