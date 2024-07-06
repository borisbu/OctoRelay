import { hasUpcomingTask } from "./narrowing";
import { describe, test, expect } from "vitest";

describe("Narrowing helpers", () => {
  describe("hasUpcomingTask() helper", () => {
    test.each([
      {
        relay: {
          relay_pin: 16,
          inverted_output: false,
          relay_state: true,
          label_text: "Nozzle Light",
          active: true,
          icon_html: "<div>&#128161;</div>",
          confirm_off: false,
          upcoming: {
            target: false,
            owner: "PRINTING_STOPPED",
            deadline: Date.now() + 150 * 1000,
          },
        },
        expected: true,
      },
      {
        relay: {
          relay_pin: 16,
          inverted_output: false,
          relay_state: true,
          label_text: "Nozzle Light",
          active: true,
          icon_html: "<div>&#128161;</div>",
          confirm_off: false,
          upcoming: {
            target: true,
            owner: "PRINTING_STOPPED",
            deadline: Date.now() + 150 * 1000,
          },
        },
        expected: false,
      },
      {
        relay: {
          relay_pin: 16,
          inverted_output: false,
          relay_state: true,
          label_text: "Nozzle Light",
          active: true,
          icon_html: "<div>&#128161;</div>",
          confirm_off: false,
          upcoming: null,
        },
        expected: false,
      },
    ])("should assert the type of the argument %#", ({ relay, expected }) => {
      expect(hasUpcomingTask(relay)).toBe(expected);
    });
  });
});
