import React from 'react';
import { Link } from 'react-router-dom';

const BreadcrumbSeperator = () => (
  <svg className="h-6 text-gray-500 dark:text-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
  </svg>
);

const BreadcrumbItem = ({ text, url }) => (
  <Link className="text-base leading-none tracking-wide text-gray-500 md:text-lg hover:text-gray-900 dark:text-white dark:hover:text-dark-primary" to={url}>{text}</Link>
);

const Breadcrumbs = ({ items }) => {
  const breadcrumbItems = [];
  // Add home item that is present in each breadcrumb
  breadcrumbItems.push(
    <BreadcrumbItem
      key="home"
      url="/"
      text={(
        <svg className="h-5 text-gray-500 md:h-6 hover:text-gray-900 dark:text-white dark:hover:text-dark-primary" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
        </svg>
      )}
    />,
  );

  items.forEach((item) => {
    breadcrumbItems.push(<BreadcrumbSeperator key={item.text + item.url} />);
    breadcrumbItems.push(
      <BreadcrumbItem
        key={item.text}
        url={item.url}
        text={item.text}
      />,
    );
  });

  return (
    <div className="flex items-center gap-1">
      {breadcrumbItems}
    </div>
  );
};

export default Breadcrumbs;
