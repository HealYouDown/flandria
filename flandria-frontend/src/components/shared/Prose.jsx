import React from 'react';

const Prose = ({ children }) => (
  <div className="flex justify-center">
    <article className="prose lg:prose-xl dark:prose-dark">
      {children}
    </article>
  </div>
);

export default Prose;
