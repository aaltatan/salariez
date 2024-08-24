/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
    'apps/**/*.{html,py}',
    'templates/**/*.html'
  ],
  safelist: [
    // cols
    'grid-cols-1',
    'grid-cols-2',
    'grid-cols-3',
    'grid-cols-4',
    'grid-cols-5',
    'grid-cols-6',
    'grid-cols-7',
    'grid-cols-8',
    'grid-cols-9',
    'grid-cols-10',
    'grid-cols-11',
    'grid-cols-12',
    // directions
    'left-1',
    'left-2',
    'left-3',
    'left-4',
    'right-1',
    'right-2',
    'right-3',
    'right-4',
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [
    require('tailwind-scrollbar')({ nocompatible: true }),
],
}

