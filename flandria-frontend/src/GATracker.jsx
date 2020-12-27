import { useEffect } from 'react';
import ReactGA from 'react-ga';
import { useLocation } from 'react-router-dom';

const GATracker = ({ children, trackingId }) => {
  const location = useLocation();
  const isDevelopment = process.env.NODE_ENV === 'development';

  const addPageView = (path) => {
    if (!isDevelopment) {
      ReactGA.pageview(path);
    }
  };

  useEffect(() => {
    // Initalize react ga
    if (!isDevelopment) {
      ReactGA.initialize(trackingId);
    }

    // Send the first page that was loaded just now
    // to GA
    addPageView(location.pathname);
  }, []);

  useEffect(() => {
    // Whenever the location changes, add a new path entry
    addPageView(location.pathname);
  }, [location]);

  return children;
};

export default GATracker;
