import { Menu, Switch, Transition } from '@headlessui/react';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getImagePath } from '../../../helpers';
import { getIdentity, isAuthenticated } from '../../auth/auth';
import ItemSearchBar from '../../shared/ItemSearchBar';
import MobileMenuButton from './MobileMenuButton';

const NavLink = ({ to, children }) => (
  <Link
    className="text-lg font-semibold text-gray-500 hover:text-gray-900 dark:text-white dark:hover:text-dark-primary"
    to={to}
  >
    {children}
  </Link>
);

const DropdownMenuLink = ({
  to, external, children, className = '',
}) => {
  const activeClassName = 'text-gray-900 bg-gray-100 dark:bg-dark-3';
  const defaultClassName = `${className} text-gray-500 w-full text-sm leading-5 text-left flex justify-between px-4 py-2 dark:text-white`;

  if (external) {
    return (
      <Menu.Item>
        {({ active }) => (
          <a
            className={`${active ? activeClassName : ''} ${defaultClassName}`}
            href={to}
            target="_blank"
            rel="noreferrer"
          >
            {children}
          </a>
        )}
      </Menu.Item>
    );
  }

  return (
    <Menu.Item>
      {({ active }) => (
        <Link
          className={`${active ? activeClassName : ''} ${defaultClassName}`}
          to={to}
          target={external ? '_blank' : ''}
          rel={external ? 'noreferrer' : ''}
        >
          {children}
        </Link>
      )}
    </Menu.Item>
  );
};

const DropdownMenu = ({
  button, children, containerClassName, itemsClassName,
}) => (
  <div className={`relative z-50 ${containerClassName}`}>
    <Menu>
      {({ open }) => (
        <>
          <Menu.Button className="flex items-center text-lg font-semibold text-gray-500 hover:text-gray-900 dark:text-white dark:hover:text-dark-primary">
            {button}
          </Menu.Button>
          <Transition
            show={open}
            enter="transition ease-out duration-100"
            enterFrom="transform opacity-0 scale-95"
            enterTo="transform opacity-100 scale-100"
            leave="transition ease-in duration-75"
            leaveFrom="transform opacity-100 scale-100"
            leaveTo="transform opacity-0 scale-95"
          >
            <Menu.Items static className={`absolute mt-2 bg-white border dark:bg-dark-2 dark:border-dark-3 border-gray-200 rounded-md shadow-md ${itemsClassName}`}>
              {children}
            </Menu.Items>
          </Transition>
        </>
      )}
    </Menu>
  </div>
);

const Nav = () => {
  const [darkModeSwitchState, setDarkModeSwitchState] = useState((localStorage.getItem('theme') || 'dark') === 'dark');
  const [isLoggedIn, setIsLoggedIn] = useState(isAuthenticated());

  const changeThemeMode = (value) => {
    const themeValue = value ? 'dark' : 'light';
    localStorage.setItem('theme', themeValue);

    window.dispatchEvent(new Event('themeChanged', { bubbles: true }));

    setDarkModeSwitchState(value);
  };

  const onStorageChange = () => {
    setIsLoggedIn(isAuthenticated());
  };

  useEffect(() => {
    window.addEventListener('storage', onStorageChange);
  }, []);

  return (
    <nav className="flex items-center h-20 gap-2 px-1 py-2 bg-white shadow-lg min-h-20 max-h-20 dark:bg-dark-1 sm:px-2 md:px-4 md:gap-4">
      <Link to="/">
        <img className="w-auto h-12" src={getImagePath('favicon.png')} alt="Flandria Logo" />
      </Link>

      <div className="flex-row items-center hidden space-x-5 lg:space-x-10 md:flex lg:ml-6">
        <NavLink to="/database/monster">Monsters</NavLink>
        <NavLink to="/database">Items</NavLink>
        <NavLink to="/database/quest">Quests</NavLink>
        <DropdownMenu
          button={(
            <>
              Planner
              <svg className="h-4 ml-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </>
        )}
          itemsClassName="divide-y w-52 left-0 dark:divide-dark-3"
        >
          <div className="py-1">
            <DropdownMenuLink to="/planner/explorer">Explorer</DropdownMenuLink>
            <DropdownMenuLink to="/planner/noble">Noble</DropdownMenuLink>
            <DropdownMenuLink to="/planner/saint">Saint</DropdownMenuLink>
            <DropdownMenuLink to="/planner/mercenary">Mercenary</DropdownMenuLink>
            <DropdownMenuLink to="/planner/ship">Ship</DropdownMenuLink>
          </div>
        </DropdownMenu>
        <DropdownMenu
          button={(
            <>
              More
              <svg className="h-4 ml-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </>
        )}
          itemsClassName="divide-y w-52 left-0 dark:divide-dark-3"
        >
          <div className="py-1">
            <DropdownMenuLink to="/map">Maps</DropdownMenuLink>
            <DropdownMenuLink to="/database/npc">NPCs</DropdownMenuLink>
          </div>
          <div className="py-1">
            <DropdownMenuLink to="/static/files/essence_system_en.pdf" external>[EN] Essence Guide</DropdownMenuLink>
            <DropdownMenuLink to="/static/files/essence_system_de.pdf" external>[DE] Essence Guide</DropdownMenuLink>
          </div>
        </DropdownMenu>
      </div>

      <ItemSearchBar inputContainerClassName="flex-grow lg:mx-5 xl:mx-12 2xl:mx-28" />

      <MobileMenuButton isLoggedIn={isLoggedIn} buttonClassName="md:hidden" />
      <DropdownMenu
        button={(
          <img
            className="w-12 h-auto border-2 border-gray-200 rounded-full min-w-min min-h-min flex-shrink-1 dark:border-dark-3"
            src={getImagePath(isLoggedIn ? 'monster_icons/lm00202.png' : 'default_login_image.png')}
            alt="Profile Icon"
          />
        )}
        containerClassName="hidden md:block"
        itemsClassName="right-0 w-52 divide-y dark:divide-dark-3"
      >
        {isLoggedIn && (
        <div className="py-1">
          <div className="flex justify-between w-full px-4 py-2 text-sm leading-5 text-left text-gray-500 dark:text-white">
            <span>
              Logged in as
              {' '}
              {getIdentity().username}
            </span>
          </div>
        </div>
        )}
        <div className="py-1">
          <Switch.Group as="div" className="flex items-center justify-between px-4 py-2">
            <Switch.Label className="text-sm text-gray-500 dark:text-white">Dark Mode</Switch.Label>
            <Switch
              as="button"
              checked={darkModeSwitchState}
              onChange={changeThemeMode}
              className={`${
                darkModeSwitchState ? 'bg-blue-600 dark:bg-dark-3' : 'bg-gray-300'
              } relative inline-flex h-4 rounded-full w-8`}
            >
              <span
                className={`${
                  darkModeSwitchState ? 'translate-x-4' : 'translate-x-0'
                } inline-block w-4 h-4 transform transition duration-200 ease-in-out bg-blue-500 dark:bg-dark-primary rounded-full`}
              />
            </Switch>
          </Switch.Group>
        </div>
        {isLoggedIn
          ? (
            <div className="py-1">
              <DropdownMenuLink className="text-red-600 dark:text-red-500" to="/auth/logout">Logout</DropdownMenuLink>
            </div>
          )
          : (
            <div className="py-1">
              <DropdownMenuLink to="/auth/login">Sign In</DropdownMenuLink>
              <DropdownMenuLink to="/auth/register">Sign Up</DropdownMenuLink>
            </div>
          )}
      </DropdownMenu>
    </nav>
  );
};

export default Nav;
