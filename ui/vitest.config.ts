import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    coverage: {
      provider: "istanbul",
      reporter: ["json", "lcov", "text", "html"],
      exclude: ["mocks", "*.config.ts", "**/*.spec.ts"],
    },
  },
});
