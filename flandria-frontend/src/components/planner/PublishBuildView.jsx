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
      <h2 className="text-3xl font-bold tracking-wide text-white uppercase mb-7">Publish a Skill-Build</h2>
      <div className="w-full max-w-md space-y-5">
        <div className={formContainerClassname}>
          <label className="text-input-label" htmlFor="url">URL (Can&apos;t be edited)</label>
          <input
            id="url"
            disabled
            className="text-input"
            value={`${window.location.host}/planner/${url_classname}/${hash}`}
          />
        </div>

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
            {500 - description.length}
            {' '}
            chars left)
          </label>
          <textarea
            maxLength={500}
            id="description"
            value={description}
            className="text-input"
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>

        <div className="flex flex-col h-12 gap-2 overflow-auto text-red-400 dark:text-red-600 max-h-12">
          {fieldErrors.map((error) => <span key={error}>{error}</span>)}
        </div>

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
