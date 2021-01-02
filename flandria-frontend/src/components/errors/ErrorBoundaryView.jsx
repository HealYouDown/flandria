import React from 'react';

const ErrorBoundaryView = ({ error }) => (
  <div className="flex justify-center py-20">
    <div role="alert" className="prose text-gray-700 dark:text-white dark:prose-dark">
      <h1>Something went really really wrong, if you see this screen. (╯°□°）╯︵ ┻━┻</h1>
      <p>The following error occured in your last action:</p>
      <pre>
        <b>{error.name}</b>
        <br />
        {error.message}
      </pre>
      <p>Feel free to report steps on how to reproduce this bug to me.</p>
      <p>
        <b>Thanks</b>
        {' '}
        in advance!
      </p>
      <p>
        You can click
        {' '}
        <a href="/">here to get back to Home</a>
        .
      </p>
      <blockquote>
        <p>
          It is human to err; and the only final and deadly error, among all our errors,
          is denying that we have ever erred.
        </p>
        <cite>- G.K. Chesterton</cite>
      </blockquote>
    </div>
  </div>
);

export default ErrorBoundaryView;
