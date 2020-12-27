import React from 'react';
import { Link } from 'react-router-dom';
import { getImagePath } from '../../helpers';

const FooterLink = ({ to, children, external }) => {
  const className = 'text-sm font-semibold text-center text-gray-500 hover:text-gray-900 dark:text-white dark:hover:text-dark-primary md:text-left';

  if (external) {
    return (
      <a
        className={className}
        href={to}
        target="_blank"
        rel="noreferrer"
      >
        {children}
      </a>
    );
  }

  return (
    <Link className={className} to={to}>
      {children}
    </Link>
  );
};

const Footer = () => (
  <footer
    className="px-5 py-2 bg-white shadow-lg md:py-6 md:px-20 lg:px-40 xl:px-60 dark:bg-dark-1"
  >
    <div className="grid items-center grid-cols-1 gap-4 md:gap-x-12 md:grid-cols-2 justify-items-center">
      <div className="max-w-sm">
        <img className="mx-auto mb-1 md:mx-0 h-14" src={getImagePath('logo.png')} alt="Logo Footer" />
        <p className="text-sm leading-tight text-center text-gray-500 md:text-left dark:text-white">
          All information on Flandria is provided as is, without any guarantee that the shown
          information is correct or up-to-date.
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-4 md:gap-x-12">
        <div className="flex flex-col">
          <h5 className="mb-1 text-sm font-bold tracking-wide text-center text-gray-700 uppercase dark:text-white md:text-left">Flandria</h5>
          <FooterLink to="/about">About Us</FooterLink>
          <FooterLink to="https://www.github.com/HealYouDown/flandria" external>Github</FooterLink>
        </div>

        <div className="flex flex-col">
          <h5 className="mb-1 text-sm font-bold tracking-wide text-center text-gray-700 uppercase dark:text-white md:text-left">Support us</h5>
          <FooterLink to="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=DWR39ZZHBKXAQ&source=url" external>Paypal</FooterLink>
          <FooterLink to="https://www.patreon.com/flandria" external>Patreon</FooterLink>
        </div>

        <div className="flex flex-col">
          <h5 className="mb-1 text-sm font-bold tracking-wide text-center text-gray-700 uppercase dark:text-white md:text-left">Discord</h5>
          <FooterLink to="https://discord.gg/zDax9Rg" external>Flandria</FooterLink>
          <FooterLink to="https://discord.gg/giikugames" external>Florensia</FooterLink>
        </div>

        <div className="flex flex-col">
          <h5 className="mb-1 text-sm font-bold tracking-wide text-center text-gray-700 uppercase dark:text-white md:text-left">Legal</h5>
          <FooterLink to="/privacy-policy">Privacy Policy</FooterLink>
          <FooterLink to="/legal-notice">Legal Notice</FooterLink>
        </div>
      </div>
    </div>
  </footer>
);

export default Footer;
