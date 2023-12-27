import { defineConfig } from "tsup";

export default defineConfig({
  entry: ["octorelay.ts"],
  outDir: "../octoprint_octorelay/static/js",
  format: "cjs",
  outExtension: () => ({ js: ".js" }),
  splitting: false,
  sourcemap: false,
  clean: true,
  dts: false,
  minify: false,
});
