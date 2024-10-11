import { readFile } from "node:fs/promises";
import { describe, test, expect } from "vitest";

describe("Integration test", () => {
  test.each(["css/octorelay.css", "js/octorelay.js"])(
    "%s build remains",
    async (file) => {
      const text = await readFile(
        `../octoprint_octorelay/static/${file}`,
        "utf8",
      );
      expect(text).toMatchSnapshot();
    },
  );
});
