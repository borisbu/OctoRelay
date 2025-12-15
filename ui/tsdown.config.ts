import { defineConfig } from "tsdown";

export default defineConfig({
  entry: ["octorelay.ts"],
  outDir: "../octoprint_octorelay/static/js",
  platform: "browser",
  target: "es6",
  sourcemap: false,
  clean: true,
  dts: false,
  minify: false,
});
