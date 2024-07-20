module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
  ],
  ignorePatterns: ["/local"], // Ignore everything except the src folder
  overrides: [
    {
      files: ['src/**/*.js'], // Apply ESLint rules only to .js files in the src folder
    },
  ],
};

