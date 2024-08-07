import globals from "globals";
import jsPlugin from "@eslint/js";
import tsPlugin from "typescript-eslint";
import prettierOverrides from "eslint-config-prettier";
import prettierRules from "eslint-plugin-prettier/recommended";
import unicornPlugin from "eslint-plugin-unicorn";
import allowedDepsPlugin from "eslint-plugin-allowed-dependencies";
import manifest from "./package.json" assert { type: "json" };

export default [
  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node, ...globals.jquery },
    },
    plugins: {
      unicorn: unicornPlugin,
      allowed: allowedDepsPlugin,
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
      "unicorn/prefer-node-protocol": "error",
    },
  },
  // For the sources
  {
    files: ["model/*.ts", "helpers/*.ts"],
    rules: {
      "allowed/dependencies": ["error", { manifest }],
    },
  },
  // For the tests
  {
    files: ["model/*.spec.ts", "helpers/*.spec.ts"],
    rules: {
      "allowed/dependencies": "off",
    },
  },
];
