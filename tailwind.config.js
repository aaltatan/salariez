/** @type {import('tailwindcss').Config} */

import fluid, { extract } from "fluid-tailwind";
const plugin = require("tailwindcss/plugin");

module.exports = {
  content: {
    files: ["apps/**/*.{html,py}", "templates/**/*.html"],
    extract: extract,
  },
  safelist: [
    // directions
    "left-1",
    "left-2",
    "left-3",
    "left-4",
    "right-1",
    "right-2",
    "right-3",
    "right-4",
    // paddings left
    "ltr:pl-1",
    "ltr:pl-2",
    "ltr:pl-3",
    "ltr:pl-4",
    "ltr:pl-5",
    "ltr:pl-6",
    "ltr:pl-7",
    "ltr:pl-8",
    "ltr:pl-9",
    "ltr:pl-10",
    "ltr:pl-11",
    "ltr:pl-12",
    // paddings right
    "rtl:pr-1",
    "rtl:pr-2",
    "rtl:pr-3",
    "rtl:pr-4",
    "rtl:pr-5",
    "rtl:pr-6",
    "rtl:pr-7",
    "rtl:pr-8",
    "rtl:pr-9",
    "rtl:pr-10",
    "rtl:pr-11",
    "rtl:pr-12",
    // border colors
    "border-green-500",
    "border-red-500",
    "border-yellow-500",
    "border-blue-500",
    "border-pink-500",
    "border-neutral-500",
    // bg colors
    "bg-green-500",
    "bg-red-500",
    "bg-yellow-500",
    "bg-blue-500",
    "bg-pink-500",
    "bg-neutral-500",
  ],
  darkMode: "class",
  theme: {
    extend: {
      animation: {
        "slow-pulse": "pulse 500ms cubic-bezier(0.4, 0, 0.6, 1) infinite",
      },
      fontFamily: {
        cairo: ["Cairo", "sans-serif"],
      },
    },
    screens: {
      sm: "40rem",
      md: "48rem",
      lg: "64rem",
      xl: "80rem",
      "2xl": "96rem",
    },
  },
  plugins: [
    require("@tailwindcss/container-queries"),
    require("@tailwindcss/forms"),
    require("tailwind-scrollbar")({ nocompatible: true }),
    plugin(function ({ addVariant }) {
      addVariant("hx-request", ["&.htmx-request"]);
    }),
    plugin(function ({ addVariant }) {
      addVariant("hx-swap", ["&.htmx-swapping"]);
    }),
    plugin(function ({ addVariant }) {
      addVariant("hx-settle", ["&.htmx-settling"]);
    }),
    plugin(function ({ addVariant }) {
      addVariant(
        "has-checked", 
        ['&:has(input[type="checkbox"][name$="-selected"]:checked)']
      );
    }),
    plugin(function ({ addVariant }) {
      addVariant(
        "has-delete-checked", 
        ['&:has(input[type="checkbox"][name$="-DELETE"]:checked)']
      );
    }),
    fluid,
  ],
};
