import React from 'react';

const ErrorBoundaryView = ({ error }) => (
  <div role="alert" className="text-gray-700 dark:text-white">
    <h1>Something went wrong</h1>
    <pre>{error.message}</pre>
  </div>
);

export default ErrorBoundaryView;
