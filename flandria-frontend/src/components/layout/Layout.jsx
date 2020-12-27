/* eslint-disable no-unused-vars */
import React, { useEffect, useState } from 'react';
import Footer from './Footer';
import Main from './Main';
import Nav from './Nav/Nav';

const Layout = ({ children }) => {
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');

  useEffect(() => {
    if (theme === 'dark') {
      document.querySelector('html').classList.add('dark');
    } else {
      document.querySelector('html').classList.remove('dark');
    }
  }, [theme]);

  const handleThemeChanged = () => {
    const themeValue = localStorage.getItem('theme') || 'dark';
    setTheme(themeValue);
  };

  useEffect(() => {
    window.addEventListener('themeChanged', handleThemeChanged);
  }, []);

  return (
    <>
      <Nav />
      <Main>
        {children}
      </Main>
      <Footer />
    </>
  );
};
export default Layout;
