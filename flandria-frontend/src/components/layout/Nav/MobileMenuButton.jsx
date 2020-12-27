import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getImagePath } from '../../../helpers';

const MobileMenuSection = ({ header, children }) => (
  <div className="py-2">
    <h5 className="mb-1 text-sm font-bold tracking-wide text-gray-900 uppercase dark:text-white">
      {header}
    </h5>
    <ul>
      {children}
    </ul>
  </div>
);

const MobileMenuLink = ({ to, children, external }) => {
  const className = 'text-sm font-semibold text-gray-500 hover:text-gray-900 dark:text-white dark:hover:text-dark-primary';

  if (external) {
    return (
      <li>
        <a
          className={className}
          href={to}
          target="_blank"
          rel="noreferrer"
        >
          {children}
        </a>
      </li>
    );
  }

  return (
    <li>
      <Link className={className} to={to}>
        {children}
      </Link>
    </li>
  );
};

const MobileSideMenu = ({ closeMenu, isLoggedIn }) => (
  <>
    <div className="absolute top-0 left-0 z-50 w-8/12 h-full max-w-xs px-2 overflow-auto bg-white divide-y dark:bg-dark-2 dark:divide-dark-3">
      <img className="w-auto h-24 p-2" src={getImagePath('logo.png')} alt="Florensia Logo" />
      <MobileMenuSection header="Navigation">
        <MobileMenuLink to="/database/monster">Monsters</MobileMenuLink>
        <MobileMenuLink to="/database">Items</MobileMenuLink>
        <MobileMenuLink to="/database/quest">Quests</MobileMenuLink>
      </MobileMenuSection>
      <MobileMenuSection header="Planner">
        <MobileMenuLink to="/planner/explorer">Explorer</MobileMenuLink>
        <MobileMenuLink to="/planner/noble">Noble</MobileMenuLink>
        <MobileMenuLink to="/planner/saint">Saint</MobileMenuLink>
        <MobileMenuLink to="/planner/mercenary">Mercenary</MobileMenuLink>
        <MobileMenuLink to="/planner/ship">Ship</MobileMenuLink>
      </MobileMenuSection>
      <MobileMenuSection header="More">
        <MobileMenuLink to="/map">Maps</MobileMenuLink>
        <MobileMenuLink to="/static/files/essence_system_en.pdf" external>[EN] Essence Guide</MobileMenuLink>
        <MobileMenuLink to="/static/files/essence_system_de.pdf" external>[DE] Essence Guide</MobileMenuLink>
      </MobileMenuSection>
      <MobileMenuSection header="Account">
        {isLoggedIn
          ? (
            <>
              <MobileMenuLink to="/auth/logout">Logout</MobileMenuLink>
            </>
          )
          : (
            <>
              <MobileMenuLink to="/auth/register">Sign Up</MobileMenuLink>
              <MobileMenuLink to="/auth/login">Sign In</MobileMenuLink>
            </>
          )}
      </MobileMenuSection>
    </div>
    <div
      onClick={closeMenu}
      role="button"
      aria-hidden="true"
      className="absolute top-0 bottom-0 left-0 right-0 z-20 bg-black opacity-30"
    />
  </>
);

const MobileMenuButton = ({ buttonClassName, isLoggedIn }) => {
  const [isOpen, setIsOpen] = useState(false);

  const handleKeydown = (event) => {
    if (event.key === 'Escape') {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    window.addEventListener('keydown', handleKeydown);
  }, [isOpen]);

  return (
    <>
      <button className={buttonClassName} type="button" onClick={() => setIsOpen(!isOpen)}>
        <svg className="w-8 h-8 text-gray-700 dark:text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
      {isOpen && (
        <MobileSideMenu
          isLoggedIn={isLoggedIn}
          closeMenu={() => setIsOpen(false)}
        />
      )}
    </>
  );
};

export default MobileMenuButton;
