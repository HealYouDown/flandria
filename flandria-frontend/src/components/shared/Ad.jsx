import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { isAuthenticated, getIdentity } from '../auth/auth';
import { getImagePath } from '../../helpers';

const Ad = ({ slot }) => {
  const location = useLocation();
  const isPremium = isAuthenticated() ? getIdentity().premium : false;
  const adblockEnabled = window.adblockEnabled || false;

  useEffect(() => {
    if (!isPremium && !adblockEnabled) {
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    }
  }, [location]);

  if (isPremium) return null;

  return (
    <div className="block mt-auto" aria-hidden>
      <div className="mt-5">
        {adblockEnabled
          ? (
            <div className="flex flex-row items-center gap-5 px-4 py-2 border-2 border-gray-700 rounded-lg sm:px-10 sm:py-4 dark:border-white">
              <img
                className="hidden h-24 rounded-full sm:block"
                src={getImagePath('ad_banner_image.png')}
                alt="crying npc"
              />
              <div>
                <span className="block mb-1 text-2xl text-gray-700 sm:text-3xl dark:text-white">Ad-Banner</span>
                <p className="text-sm leading-none text-gray-500 whitespace-normal dark:text-white dark:text-opacity-70">
                  This would be an ad-banner, if you had adblock disabled.
                  <br />
                  Ads help me pay the hosting fees to keep Flandria up and running.
                  Please consider whitelisting this page to support Flandria.
                </p>
              </div>
            </div>
          )
          : (
            <ins
              className="w-full adsbygoogle h-28"
              data-ad-client="ca-pub-7852193310298972"
              data-ad-slot={slot.toString()}
              data-ad-format="auto"
              data-full-width-responsive="true"
            />
          )}
      </div>
    </div>
  );
};

export default Ad;
