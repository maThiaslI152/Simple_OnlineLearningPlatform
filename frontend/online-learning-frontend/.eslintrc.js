module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    'plugin:prettier/recommended' // Add this
  ],
  plugins: ['prettier'],
  rules: {
    'prettier/prettier': ['error', { endOfLine: 'lf' }], // Enforce line ending rule
  },
};
