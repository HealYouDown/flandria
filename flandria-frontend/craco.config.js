module.exports = {
  style: {
    postcss: {
      plugins: [
        require('tailwindcss'), //eslint-disable-line
        require('autoprefixer'), //eslint-disable-line
      ],
    },
  },
};
