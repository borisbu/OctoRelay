import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    coverage: {
      enabled: true,
      provider: "istanbul",
      reporter: ["json", "lcov", "text", "html"],
      exclude: ["mocks"],
    },
  },
});
