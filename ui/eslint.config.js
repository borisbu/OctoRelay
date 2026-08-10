import globals from "globals";
import jsPlugin from "@eslint/js";
import tsPlugin from "typescript-eslint";
import allowedDepsPlugin from "eslint-plugin-allowed-dependencies";
import { builtinModules } from "node:module";

export default [
  {
    languageOptions: {
      globals: { ...globals.browser, ...globals.node, ...globals.jquery },
    },
    plugins: {
      allowed: allowedDepsPlugin,
    },
  },
  jsPlugin.configs.recommended,
  ...tsPlugin.configs.recommended,
  // Things to turn off globally
  { ignores: ["coverage/", "styles/"] },
  // Things to turn on globally
  {
    rules: {
      "no-restricted-syntax": [
        "error",
        ...builtinModules.map((mod) => ({
          selector: `ImportDeclaration[source.value='${mod}']`,
          message: `use node:${mod} for the built-in module`,
        })),
      ],
    },
  },
  // For the sources
  {
    files: ["model/*.ts", "helpers/*.ts"],
    rules: {
      "allowed/dependencies": "error",
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
