import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Transition } from '@headlessui/react';
import { Link } from 'react-router-dom';
import { useDebouncedCallback } from 'use-debounce';
import { getApiUrl, tablenameToTitle } from '../../helpers';
import Icon from './Icon';
import ItemSubs from './ItemSubs';
import ItemDuration from './ItemDuration';

const SearchResultItem = ({ tableKey, item, onItemClick }) => {
  let rareGrade = 0;
  let tablename = '';
  let isItemListTable = false;
  let toUrl = '';

  switch (tableKey) {
    case 'monsters':
      rareGrade = item.rating.value;
      tablename = 'monster';
      toUrl = `/database/monster/${item.code}`;
      break;
    case 'npcs':
      tablename = 'npc';
      toUrl = `/database/npc/${item.code}`;
      break;
    case 'quests':
      tablename = 'quest';
      toUrl = `/database/quest/${item.code}`;
      break;
    case 'guilds':
      tablename = 'guild';
      toUrl = encodeURI(encodeURI(`/ranking/guilds/${item.name}`));
      break;
    case 'players':
      tablename = 'player';
      toUrl = `/ranking/players/${item.server.value === 0 ? 'luxplena' : 'bergruen'}/${item.name}`;
      break;
    default:
      rareGrade = item.rare_grade;
      tablename = item.table;
      isItemListTable = true;
      toUrl = `/database/${tablename}/${item.code}`;
  }

  return (
    <Link
      to={toUrl}
      onClick={onItemClick}
      className="flex items-center px-3 py-1 rounded-md group hover:bg-gray-200 dark:hover:bg-dark-3"
    >
      <Icon
        icon={item.icon}
        tablename={tablename}
        rareGrade={rareGrade}
        className="group-hover:border-opacity-100 w-8 h-8 mr-1.5 box-content"
      />
      <div className="flex flex-col">
        <span className="text-sm font-semibold leading-none text-gray-700 group-hover:text-gray-900 dark:text-white dark:group-hover:text-white">
          {item.name || item.title}
          <ItemDuration className="text-sm" duration={item.duration} />
        </span>
        <ItemSubs tablename={tablename} item={isItemListTable ? item.item_data : item} />
      </div>
    </Link>
  );
};

const SearchResultSection = ({ tableKey, items, onItemClick }) => {
  if (items.length === 0) {
    return null;
  }

  return (
    <div className="py-2">
      <span className="text-lg font-semibold tracking-wide text-gray-900 dark:text-white">
        {tablenameToTitle(tableKey)}
      </span>
      <div className="grid grid-cols-1 gap-0 xl:grid-cols-2 xl:gap-1 2xl:grid-cols-3">
        {items.map((item) => (
          <SearchResultItem
            onItemClick={onItemClick}
            key={item.code}
            tableKey={tableKey}
            item={item}
          />
        ))}
      </div>
    </div>
  );
};

const ItemSearchBar = ({ inputContainerClassName = '', resultContainerClassName = '' }) => {
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState({});
  const [hasFocus, setHasFocus] = useState(false);

  // Debounced search callback
  const debouncedSearch = useDebouncedCallback((searchString) => {
    if (searchString.length < 1) {
      setSearchResults({});
      setIsSearching(false);
      return;
    }

    const url = `${getApiUrl()}/database/search?s=${searchString}`;
    const fetchSearchResults = async () => {
      setIsSearching(true);
      const result = await axios(url);
      setSearchResults(result.data);
      setIsSearching(false);
    };

    fetchSearchResults();
  }, 300);

  // Refs for click away event
  const inputRef = useRef();
  const resultsRef = useRef();

  // Handles clicks when the search is open. If none of the search
  // elements were clicked, it will close the search.
  const handleClick = (event) => {
    // Check if both refs exist.
    if (inputRef.current && resultsRef.current) {
      // That means the popup is open
      // Now check if the clicked element is not inside
      // any of the refs.
      if (!inputRef.current.contains(event.target) && !resultsRef.current.contains(event.target)) {
        setHasFocus(false);
      }
    }
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClick);
  }, []);

  const onItemClick = () => {
    setHasFocus(false);
  };

  return (
    <div className={`relative z-50 ${inputContainerClassName}`}>
      <div className="flex items-center px-2 py-1 border-2 border-gray-200 rounded-lg dark:border-dark-3">
        <div className="mr-2">
          {isSearching ? (
            <svg className="w-5 h-5 text-gray-400 dark:text-white animate-spin" viewBox="0 0 24 24">
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
          ) : (
            <svg className="w-5 h-5 text-gray-400 dark:text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          )}
        </div>
        <input
          type="search"
          ref={inputRef}
          onFocus={() => setHasFocus(true)}
          onChange={(e) => debouncedSearch.callback(e.target.value)}
          placeholder="Search..."
          className="flex-grow w-full min-w-0 bg-transparent outline-none dark:text-white"
        />
      </div>
      <Transition
        show={(Object.keys(searchResults).length > 0 && hasFocus)}
        enter="transition ease-out duration-100"
        enterFrom="transform opacity-0 scale-95"
        enterTo="transform opacity-100 scale-100"
        leave="transition ease-in duration-75"
        leaveFrom="transform opacity-100 scale-100"
        leaveTo="transform opacity-0 scale-95"
      >
        <div
          className={
            `absolute bg-white w-full mt-2 px-3 rounded-lg shadow-md max-h-96 overflow-y-auto divide-y dark:divide-dark-3 border-gray-200 border dark:border-dark-3 dark:bg-dark-2
            ${resultContainerClassName}`
          }
          ref={resultsRef}
        >
          {Object.keys(searchResults).map((key) => (
            <SearchResultSection
              key={key}
              tableKey={key}
              onItemClick={onItemClick}
              items={searchResults[key]}
            />
          ))}
        </div>
      </Transition>
    </div>
  );
};

export default ItemSearchBar;
