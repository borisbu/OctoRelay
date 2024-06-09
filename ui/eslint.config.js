import globals from "globals";
import jsPlugin from "@eslint/js";
import tsPlugin from "typescript-eslint";
import prettierOverrides from "eslint-config-prettier";
import prettierRules from "eslint-plugin-prettier/recommended";
import unicornPlugin from "eslint-plugin-unicorn";
import importPlugin from "eslint-plugin-import-x";

export default [
  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node, ...globals.jquery },
    },
    plugins: {
      unicorn: unicornPlugin,
      "import-x": importPlugin,
    },
  },
  jsPlugin.configs.recommended,
  ...tsPlugin.configs.recommended,
  prettierOverrides,
  prettierRules,
  // Things to turn off globally
  { ignores: ["coverage/", "styles/"] },
  // Things to turn on globally
  {
    rules: {
      "import-x/named": "error",
      "import-x/export": "error",
      "import-x/no-duplicates": "warn",
      "unicorn/prefer-node-protocol": "error",
    },
  },
  // For the sources
  {
    files: ["model/*.ts", "helpers/*.ts"],
    rules: {
      "import-x/no-extraneous-dependencies": "error",
    },
  },
];
