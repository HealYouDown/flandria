import React from 'react';
import { getImagePath } from '../../helpers';

const AuthWrapper = ({ children }) => (
  <div className="flex justify-center">
    <div className="flex flex-grow max-w-4xl bg-white border-l-4 border-blue-400 rounded-md shadow-xl dark:bg-dark-3">
      <div className="flex flex-col items-center w-full gap-4 px-4 py-4 md:w-6/12 md:gap-12 lg:px-20 lg:py-10">
        {children}
      </div>
      <div className="hidden md:block md:w-6/12">
        <img
          className="object-cover w-full h-full rounded-r-md"
          src={getImagePath('artworks/serbetus.jpeg')}
          alt="Login view side"
        />
      </div>
    </div>
  </div>
);

export default AuthWrapper;
