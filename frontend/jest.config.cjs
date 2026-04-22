module.exports = {
  moduleFileExtensions: ['js', 'jsx', 'json', 'vue'],
  transform: {
    '^.+\\.vue$': '@vue/vue3-jest',
    '^.+\\.(js|jsx)$': 'babel-jest',
    '.+\\.(css|styl|less|sass|scss|svg|png|jpg|ttf|woff|woff2)$': 'jest-transform-stub',
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^~/(.*)$': '<rootDir>/tests/unit/factories/$1',
    '\\.(css|less|sass|scss)$': 'jest-transform-stub',
    '\\.(gif|ttf|eot|svg|png)$': 'jest-transform-stub',
  },
  testEnvironment: 'jest-environment-jsdom',
  testEnvironmentOptions: {
    customExportConditions: ['node', 'node-addons', 'require', 'default'],
  },
  transformIgnorePatterns: [
    'node_modules[/\\\\](?!(vue|@vue|pinia|vue-router|vue-i18n|vue-toastification|@vee-validate|vee-validate|axios|bootstrap-vue-next|@fortawesome|js-cookie|moment)[/\\\\])',
  ],
  testMatch: [
    '**/tests/unit/**/*.spec.(js|jsx|ts|tsx)',
    '**/__tests__/*.(js|jsx|ts|tsx)',
  ],
  collectCoverage: false,
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: -10,
    },
  },
  collectCoverageFrom: [
    '**/src/**/*.{js,vue}',
    '!**/src/main.js',
    '!**/src/router.js',
    '!**/src/stores/index.js',
    '!**/node_modules/**',
  ],
  setupFiles: ['jest-date-mock'],
};
