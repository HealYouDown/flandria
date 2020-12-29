import React from 'react';
import { getImagePath, setWindowTitle } from '../../helpers';

const LandingPage = () => {
  setWindowTitle('Home');

  return (
    <div className="flex flex-col items-center justify-center gap-y-10 lg:gap-20 lg:flex-row">
      <div className="max-w-3xl">
        <span className="text-2xl tracking-wide text-gray-500 dark:text-white dark:text-opacity-90">Your Florensia Database</span>
        <h2 className="mt-3 mb-5 text-5xl font-semibold tracking-tight text-gray-700 lg:text-8xl dark:text-white">Flandria</h2>
        <p className="max-w-lg text-base font-thin leading-7 text-gray-500 dark:text-white dark:text-opacity-70">
          Flandria is an open-source database website for the MMORPG Florensia.
          It provides a clean interface to view all available monsters, items and quest in the
          world of Florensia.
          Also included is a character builder, which allows you to design your own character
          skilltree as well as maps, where you can view the locations of all monster.
        </p>
      </div>

      <div className="max-w-md">
        <img className="rounded-full" src={getImagePath('landing_page_image_small.png')} alt="Landing Page" />
      </div>
    </div>
  );
};

export default LandingPage;
