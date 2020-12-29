import React from 'react';

const Main = ({ children }) => (
  <main className="flex flex-col flex-grow px-4 py-8 md:px-10 lg:px-20 xl:px-40">
    {children}
  </main>
);
export default Main;
