/* eslint-disable no-unused-vars */
import React from 'react';
import { useCookies } from 'react-cookie';
import { HiOutlineX } from 'react-icons/hi';

// onLoad={setCookie('donate_banner', 0, { path: '/', maxAge: 7884000 })}

const DonateBanner = () => {
  const [, setCookie] = useCookies();

  return (
    <div className="fixed bottom-0 right-0 z-50 bg-white border border-gray-200 rounded-sm shadow-2xl md:max-w-lg md:right-4 md:bottom-4 dark:bg-dark-3 dark:border-dark-4">
      <div className="relative px-10 py-5">
        <button
          type="button"
          className="absolute top-3 right-3 dark:text-white"
          onClick={() => setCookie('donate_banner', 0, { path: '/', maxAge: 5256000, secure: true })}
        >
          <HiOutlineX className="w-5 h-5 animate-bounce" />
        </button>
        <span className="text-2xl font-semibold text-gray-900 dark:text-white">Support us! ❤</span>
        <p className="text-gray-700 dark:text-white dark:text-opacity-70">
          Flandria does
          {' '}
          <b>not</b>
          {' '}
          show any ads. However, things like the domain and hosting still cost money.
          <br />
          <br />
          If you love Flandria and want to support the project, click below to do a donation!
        </p>
        <div className="flex gap-4 mt-5">
          <a
            href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DWR39ZZHBKXAQ&source=url"
            target="_blank"
            rel="noreferrer"
            className="px-5 py-2 text-lg font-semibold text-white bg-blue-500 rounded-md hover:bg-blue-600"
          >
            PayPal
          </a>
          <a
            href="https://www.patreon.com/flandria"
            target="_blank"
            rel="noreferrer"
            className="px-5 py-2 text-lg font-semibold text-white bg-red-500 rounded-md hover:bg-red-600"
          >
            Patreon
          </a>
        </div>
      </div>
    </div>
  );
};

export default DonateBanner;
