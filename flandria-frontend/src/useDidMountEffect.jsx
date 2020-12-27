import { useEffect, useRef } from 'react';

// See why and what it does here:
// https://stackoverflow.com/questions/53253940/make-react-useeffect-hook-not-run-on-initial-render

const useDidMountEffect = (func, deps) => {
  const didMount = useRef(false);

  useEffect(() => {
    if (didMount.current) func();
    else didMount.current = true;
  }, deps);
};

export default useDidMountEffect;
