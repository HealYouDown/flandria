/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable camelcase */
import React, { useEffect, useState } from 'react';
import { HiCursorClick } from 'react-icons/hi';
import { useHistory, useLocation } from 'react-router-dom';
import Axios from 'axios';
import { getApiUrl, setWindowTitle } from '../../helpers';
import { getToken } from '../auth/auth';

const formContainerClassname = 'flex flex-col flex-grow space-y-2';

const PublishBuildView = () => {
  const location = useLocation();
  const history = useHistory();

  useEffect(() => {
    setWindowTitle('Publish a build');
  }, []);

  if (!location.state) {
    history.push('/');
    return null;
  }

  const { url_classname, character_class, hash } = location.state;

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [fieldErrors, setFieldErrors] = useState([]);

  const publishBuild = async () => {
    setFieldErrors([]);

    if (title.length <= 2) {
      setFieldErrors(['Field Title is too short.']);
      return null;
    }

    try {
      await Axios.post(`${getApiUrl()}/planner/builds/add`, {
        title,
        description,
        hash,
        character_class,
      }, {
        headers: { Authorization: `Bearer ${getToken()}` },
      });
      history.push(`/planner/${url_classname}/builds`);
    } catch (error) {
      const errorMessage = error.response.data.message;
      setFieldErrors([errorMessage]);
    }

    return null;
  };

  return (
    <div className="flex flex-col items-center justify-center w-full">
      <div className="w-full max-w-2xl px-8 py-4 space-y-5 bg-white border-l-4 border-blue-400 rounded-md shadow-xl dark:bg-dark-3">
        <h2 className="w-full text-3xl font-bold tracking-wide text-center text-gray-900 uppercase dark:text-white mb-7">Publish a Skill-Build</h2>
        <div className={formContainerClassname}>
          <label className="text-input-label" htmlFor="title">
            Title * (
            {50 - title.length}
            {' '}
            chars left)
          </label>
          <input
            id="title"
            value={title}
            className="text-input"
            maxLength={50}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div className={formContainerClassname}>
          <label className="text-input-label" htmlFor="description">
            Description (
            {700 - description.length}
            {' '}
            chars left)
          </label>
          <textarea
            maxLength={700}
            id="description"
            value={description}
            className="text-input"
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        <p className="text-gray-500 dark:text-white dark:text-opacity-75">
          Publish build for
          {' '}
          <a
            className="text-blue-500 dark:text-blue-400"
            href={`/planner/${url_classname}#${hash}`}
            target="_blank"
            rel="noreferrer"
            style={{ overflowWrap: 'anywhere' }}
          >
            {`${window.location.host}/planner/${url_classname}#${hash}`}
          </a>
        </p>

        {fieldErrors.length > 0 && (
        <div className="flex flex-col h-12 gap-2 overflow-auto text-red-400 dark:text-red-600 max-h-12">
          {fieldErrors.map((error) => <span key={error}>{error}</span>)}
        </div>
        )}

        <button
          type="button"
          onClick={publishBuild}
          className="flex items-center justify-center w-full gap-1 px-2 py-1 text-lg text-white bg-blue-400 rounded-md hover:bg-blue-500"
        >
          <HiCursorClick className="w-4 h-4" />
          Publish
        </button>

      </div>
    </div>
  );
};

export default PublishBuildView;
