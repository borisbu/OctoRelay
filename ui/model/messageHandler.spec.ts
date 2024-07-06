import { elementMock, jQueryMock } from "../mocks/jQuery";
import type { OwnModel, OwnProperties } from "../types/OwnModel";
import { clearMock, showMock } from "../mocks/hints";
import { toggleMock } from "../mocks/actions";
import { makeMessageHandler } from "./messageHandler";
import { describe, vi, type Mock, afterEach, test, expect } from "vitest";

describe("makeMessageHandler()", () => {
  Object.assign(global, {
    $: jQueryMock,
  });

  afterEach(() => {
    jQueryMock.mockClear();
    toggleMock.mockClear();
    clearMock.mockClear();
    showMock.mockClear();
    elementMock.on.mockClear();
  });

  const initialize = (hasPermissionMock?: Mock) => {
    const handler = makeMessageHandler({
      settingsViewModel: {
        access: {
          permissions: {
            PLUGIN_OCTORELAY_SWITCH: "I am PLUGIN_OCTORELAY_SWITCH",
          },
        },
      },
      loginState: { hasPermission: hasPermissionMock },
    } as unknown as OwnModel & OwnProperties);
    return { handler, hasPermissionMock };
  };

  test("should ignore messages addressed to another plugins", () => {
    const { handler } = initialize();
    handler("test", {});
    expect(jQueryMock).not.toHaveBeenCalled();
  });

  test("should avoid showing buttons when can not figure out the permission", () => {
    const { handler, hasPermissionMock } = initialize(); // no implementation given
    handler("octorelay", {
      r1: {
        relay_pin: 16,
        inverted_output: false,
        relay_state: true,
        label_text: "Nozzle Light",
        active: true,
        icon_html: "<div>&#128161;</div>",
        confirm_off: false,
        upcoming: null,
      },
    });
    expect(hasPermissionMock).toBeUndefined(); // could not be called
    expect(elementMock.toggle).toHaveBeenLastCalledWith(false);
    expect(clearMock).toHaveBeenCalled();
    expect(showMock).toHaveBeenCalled();
  });

  test("Should not show buttons without permission", () => {
    const { handler, hasPermissionMock } = initialize(vi.fn(() => false));
    handler("octorelay", {
      r1: {
        relay_pin: 16,
        inverted_output: false,
        relay_state: true,
        label_text: "Nozzle Light",
        active: true,
        icon_html: "<div>&#128161;</div>",
        confirm_off: false,
        upcoming: null,
      },
    });
    expect(hasPermissionMock).toHaveBeenCalledWith(
      "I am PLUGIN_OCTORELAY_SWITCH",
    );
    expect(elementMock.toggle).toHaveBeenLastCalledWith(false);
    expect(clearMock).toHaveBeenCalled();
    expect(showMock).toHaveBeenCalled();
  });

  test("Should not show buttons for inactive relays", () => {
    const { handler } = initialize(vi.fn(() => true));
    handler("octorelay", {
      r1: {
        relay_pin: 16,
        inverted_output: false,
        relay_state: true,
        label_text: "Nozzle Light",
        active: false,
        icon_html: "<div>&#128161;</div>",
        confirm_off: false,
        upcoming: null,
      },
    });
    expect(elementMock.toggle).toHaveBeenLastCalledWith(false);
    expect(clearMock).toHaveBeenCalled();
    expect(showMock).toHaveBeenCalled();
  });

  test("Should activate the controls and set click handlers", () => {
    const { handler } = initialize(vi.fn(() => true));
    handler("octorelay", {
      r1: {
        relay_pin: 16,
        inverted_output: false,
        relay_state: true,
        label_text: "Nozzle Light",
        active: true,
        icon_html: "<div>&#128161;</div>",
        confirm_off: false,
        upcoming: null,
      },
    });
    expect(elementMock.toggle).toHaveBeenLastCalledWith(true);
    expect(clearMock).toHaveBeenCalled();
    expect(showMock).toHaveBeenCalled();
    expect(elementMock.on).toHaveBeenCalledTimes(1);
    expect(toggleMock).not.toHaveBeenCalled();
    const onClick = elementMock.on.mock.calls[0][1];
    onClick();
    expect(toggleMock).toHaveBeenCalledWith("r1", {
      active: true,
      confirm_off: false,
      icon_html: "<div>&#128161;</div>",
      inverted_output: false,
      label_text: "Nozzle Light",
      relay_pin: 16,
      relay_state: true,
      upcoming: null,
    });
  });
});
