/* eslint-disable prettier/prettier */
import { readFileSync } from "node:fs";
import { JSDOM } from "jsdom";

describe("Knockout bindings", () => {
  const html = readFileSync(
    "../octoprint_octorelay/templates/octorelay_settings.jinja2",
    "utf-8"
  );
  const document = JSDOM.fragment(html);
  const settingRegex = /^settings\.plugins\.octorelay\.r\{\{n\}\}.(\w+)$/;
  const relaySettings = [
    "active",
    "relay_pin",
    "inverted_output",
    "initial_value",
    "label_text",
    "cmd_on",
    "cmd_off",
    "auto_on_before_print",
    "auto_off_after_print",
    "auto_off_delay",
    "icon_on",
    "icon_off",
    "confirm_off"
  ];

  test("Settings template should have bindings to the correctly named settings", () => {
    const elements = Array.from(document.querySelectorAll("[data-bind]"));
    expect(elements.length).toBeGreaterThan(0);
    for (const element of elements) {
      const bindings = element.getAttribute("data-bind")?.split(",") || [];
      expect(bindings.length).toBeGreaterThan(0);
      for (const binding of bindings) {
        const [{}, address] = binding.trim().split(":");
        expect(settingRegex.test(address.trim())).toBeTruthy();
        const match = address.trim().match(settingRegex);
        const relaySetting = match?.[1];
        expect(typeof relaySetting).toBe("string");
        if (relaySetting) {
          expect(relaySettings.includes(relaySetting)).toBeTruthy();
        }
      }
    }
  });
});
