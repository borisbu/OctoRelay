import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    coverage: {
      provider: "v8",
      reporter: ["json", "lcov", "text", "html"],
      exclude: ["mocks", "*.config.ts"],
    },
  },
});
