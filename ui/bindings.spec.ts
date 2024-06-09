import { readFileSync } from "node:fs";
import { JSDOM } from "jsdom";
import { describe, test, expect } from "vitest";

describe("Knockout bindings", () => {
  const html = readFileSync(
    "../octoprint_octorelay/templates/octorelay_settings.jinja2",
    "utf-8",
  );
  const document = JSDOM.fragment(html);
  const usingContexts = [
    "settings.plugins.octorelay.r{{n}}",
    "settings.plugins.octorelay",
    "r{{n}}",
    "rules.{{event}}",
  ];
  const settingRegex = /([\w{}]+).*$/;
  const relaySettings = [
    "active",
    "relay_pin",
    "inverted_output",
    "label_text",
    "cmd_{{state}}", // on/off added programmatically
    "icon_{{state}}", // on/off added programmatically
    "confirm_off",
    "show_upcoming",
    "state",
    "delay",
  ];
  const parentSettings = ["$parent.common.printer"];

  test("Settings template should have bindings to the correctly named settings", () => {
    const elements = Array.from(document.querySelectorAll("[data-bind]"));
    expect(elements.length).toBeGreaterThan(0);
    for (const element of elements) {
      const bindings = element.getAttribute("data-bind")?.split(",") || [];
      expect(bindings.length).toBeGreaterThan(0);
      for (const binding of bindings) {
        const [keyword, address] = binding.trim().split(":");
        if (["checkedValue", "css"].includes(keyword)) {
          continue;
        }
        if (keyword === "using") {
          expect(usingContexts.includes(address.trim())).toBeTruthy();
          continue;
        }
        expect(settingRegex.test(address.trim())).toBeTruthy();
        if (address.trim().startsWith("$parent")) {
          expect(parentSettings.includes(address));
          continue;
        }
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
