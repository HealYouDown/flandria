import React from 'react';
import { useLocation } from 'react-router-dom';

const PublishBuildView = (props) => {
  console.log(props);
  const location = useLocation();

  console.log(location);

  return (
    <div>
      <h1>Publish Build</h1>
    </div>
  );
};

export default PublishBuildView;
