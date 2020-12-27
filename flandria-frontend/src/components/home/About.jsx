import React, { useEffect } from 'react';
import { setWindowTitle } from '../../helpers';
import Prose from '../shared/Prose';

const About = () => {
  useEffect(() => {
    setWindowTitle('About');
  }, []);

  return (
    <Prose>
      <h1 className="sr-only">About</h1>
      <h2>What is Flandria?</h2>
      <p>
        Flandria is a project that started late 2018 with the goal to make a good
        Florensia database website. It was then first released on the first of January 2019.
        <br />
        Even today, it is still in development and maintained on a regular basis to reflect
        the newest patches.
      </p>

      <h2>Is Flandria associated with GiikuGames?</h2>
      <p>
        Flandria is not a product by GiikuGames and they, as the Publisher of Florensia,
        have no say over what is supposed to go on this website.
        <br />
        However, from time to time they support the project by advertisments or by placing
        a link on their website.
      </p>

      <h2>How does Flandria work?</h2>
      <p>
        Obviously, adding all information manually would require months, keeping them up to
        date even more.
        <br />
        Therefore, Flandria takes all its data (except drops) from the game client. This is
        done fully automatically.
        <br />
        <blockquote>
          Credits go to
          {' '}
          <a href="https://github.com/Flauschbaellchen">Noxx</a>
          , which scripts were available on Github and allowed me to
          implement those algorithms without having to figure everything out
          from scratch.
        </blockquote>
      </p>
      <h3>Stack</h3>
      <p>
        Flandria consists of a Frontend and Backend that are seperated from each other -
        the backend is written in
        {' '}
        <a href="https://flask.palletsprojects.com/en/1.1.x/">Flask</a>
        ,
        while the Frontend uses
        {' '}
        <a href="https://reactjs.org/">ReactJS</a>
        .
      </p>
      <h3>Github</h3>
      <p>
        Flandria is completly open-source and avaialable on Github.
        You are free to contribute.
        <br />
        If you have no coding experience but want to help out, you can
        do this by joining our
        {' '}
        <a href="https://discord.gg/zDax9Rg">Discord</a>
        {' '}
        and help us collect all the (still)
        missing drops.
      </p>

      <h2>About me</h2>
      <blockquote>
        Text from late 2020, may not be up to date whenver you read this. 🤷‍♂️
      </blockquote>
      <p>
        Hi! My name is Jeremy, I am 20 years old and live in Germany. Currently,
        I am working as a Software Developer.
        <br />
        I started Flandria as a project to learn and never thought it would reach the state
        it is in today, but that gives me even more possibilities to learn from.
        <br />
        I play Florensia for about 8 years now, but probably not that active as I used to.
        You can find me on Bergruen as
        {' '}
        <b>Shadow</b>
        .
        <br />
        If you have any questions about this project, feel free to add me on Discord:
        <b> Jeremy#8813</b>
        .
      </p>
    </Prose>
  );
};

export default About;
