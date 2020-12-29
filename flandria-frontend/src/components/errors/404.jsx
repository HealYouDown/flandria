import React, { useEffect } from 'react';
import { getImagePath, setWindowTitle } from '../../helpers';

const Error404Page = () => {
  useEffect(() => {
    setWindowTitle('Error 404');
  }, []);

  return (
    <div className="flex items-center justify-center w-full h-full">
      <div className="flex flex-col items-center max-w-xl text-center md:flex-row">
        <img
          className="mr-2 rounded-full w-52 h-52"
          src={getImagePath('404_error_image.png')}
          alt="404 error fungi"
        />
        <div>
          <h2 className="text-3xl text-gray-900 dark:text-white">
            <span className="font-semibold">404</span>
            {' '}
            - Page not found
          </h2>
          <small className="mt-2 text-gray-500 dark:text-white dark:text-opacity-70">
            You are seeing this error because you tried to visit a page
            that does not exist.
          </small>
        </div>
      </div>
    </div>
  );
};

export default Error404Page;
