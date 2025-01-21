module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    "plugin:vue/vue3-essential",
    "eslint:recommended",
    "@vue/typescript/recommended",
    // "plugin:prettier/recommended",
    "prettier",
  ],
  parserOptions: {
    ecmaVersion: 2020,
  },
  rules: {
    "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "warn" : "off",
    "vue/multi-word-component-names": "off",
    "@typescript-eslint/no-var-requires": "off",
    "vue/no-reserved-component-names": "off",
    quotes: ["error", "double"],
    // https://eslint.vuejs.org/user-guide/#conflict-with-prettier
    "vue/html-indent": "off",
    "@typescript-eslint/no-require-imports": "off",
  },
};
