/* eslint-disable global-require */
module.exports = {
  purge: {
    content: [
      './src/**/*.js',
      './src/**/*.jsx',
      './public/*.html',
    ],
    options: {
      safelist: [/col-span-/, /react-select__/],
    },
  },
  darkMode: 'class',
  theme: {
    extend: {
      typography: (theme) => ({
        dark: {
          css: {
            color: 'rgba(255, 255, 255, 0.7)',
            a: {
              color: theme('colors.dark-primary'),
            },
            h1: {
              color: theme('colors.white'),
            },
            h2: {
              color: theme('colors.white'),
            },
            h3: {
              color: theme('colors.white'),
            },
            h4: {
              color: theme('colors.white'),
            },
            h5: {
              color: theme('colors.white'),
            },
            h6: {
              color: theme('colors.white'),
            },
            blockquote: {
              color: 'rgba(255, 255, 255, 0.7)',
            },
          },
        },
      }),
      height: {
        'min-content': 'min-content',
      },
      minHeight: {
        20: '5rem',
        112: '40rem',
      },
      maxHeight: {
        112: '40rem',
      },
      borderWidth: {
        3: '3px',
      },
      colors: {
        'monster-grade-1': '#7fce2e',
        'monster-grade-2': '#cf304e',
        'monster-grade-3': '#e7b23f',
        'item-grade-0': '#99ccff',
        'item-grade-1': '#99e680',
        'item-grade-2': '#e6cc99',
        'item-grade-3': '#ffbd8f',
        'dark-1': '#212121',
        'dark-2': '#303030',
        'dark-3': '#424242',
        'dark-4': '#525252',
        'dark-primary': 'teal',
      },
      keyframes: {
        scale: {
          '0%%': { transform: 'scale(1.0)' },
          '100%': { transform: 'scale(1.05)' },
        },
      },
      animation: {
        scale: 'scale 0.2s linear forwards',
      },
    },
  },
  variants: {
    extend: {
      typography: ['dark'],
      animation: ['hover'],
      backgroundImage: ['hover'],
      textOpacity: ['dark'],
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
