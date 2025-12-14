import { defineConfig } from "tsdown";

export default defineConfig({
  entry: ["octorelay.ts"],
  outDir: "../octoprint_octorelay/static/js",
  format: "cjs",
  outExtensions: () => ({ js: ".js" }),
  platform: "browser",
  sourcemap: false,
  clean: true,
  dts: false,
  minify: false,
  target: "es6",
});
