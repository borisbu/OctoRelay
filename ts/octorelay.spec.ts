import MockDate from "mockdate";
import type { OwnModel, OwnProperties } from "./types/OwnModel";

describe("OctoRelayViewModel", () => {
  const registry: ViewModel[] = [];
  const elementMock: Record<
    | "toggle"
    | "html"
    | "off"
    | "on"
    | "find"
    | "text"
    | "modal"
    | "tooltip"
    | "popover"
    | "closest"
    | "is",
    jest.Mock
  > = {
    toggle: jest.fn(() => elementMock),
    html: jest.fn(() => elementMock),
    off: jest.fn(() => elementMock),
    on: jest.fn(() => elementMock),
    find: jest.fn(() => elementMock),
    text: jest.fn(() => elementMock),
    modal: jest.fn(() => elementMock),
    tooltip: jest.fn(() => elementMock),
    popover: jest.fn(() => elementMock),
    closest: jest.fn(() => elementMock),
    is: jest.fn(() => true),
  };
  const jQueryMock = jest.fn((subject: string | (() => void)) => {
    if (typeof subject === "function") {
      return subject();
    }
    return elementMock;
  });
  const apiMock = jest.fn();
  const permissionsMock: Partial<Record<"PLUGIN_OCTORELAY_SWITCH", object>> = {
    PLUGIN_OCTORELAY_SWITCH: { test: "I am PLUGIN_OCTORELAY_SWITCH" },
  };
  const hasPermissionMock = jest.fn();
  const setIntervalMock = jest.fn<void, [() => void, number]>(
    () => "mockedInterval"
  );
  const clearIntervalMock = jest.fn();
  const addEventListenerMock = jest.fn();
  const removeEventListenerMock = jest.fn();

  Object.assign(global, {
    LOCALE: "en",
    OCTOPRINT_VIEWMODELS: registry,
    OctoPrint: { simpleApiCommand: apiMock },
    $: jQueryMock,
    document: {
      addEventListener: addEventListenerMock,
      removeEventListener: removeEventListenerMock,
    },
    setInterval: setIntervalMock,
    clearInterval: clearIntervalMock,
  });
  require("./octorelay");

  beforeAll(() => {
    const [model] = registry;
    const { construct } = model;
    construct.call(construct, [
      { access: { permissions: permissionsMock } },
      { hasPermission: hasPermissionMock },
    ]);
  });

  afterEach(() => {
    MockDate.set("2023-08-13T22:30:00");
    jQueryMock.mockClear();
    elementMock.tooltip.mockClear();
    elementMock.popover.mockClear();
    elementMock.on.mockClear();
    elementMock.text.mockClear();
    setIntervalMock.mockClear();
    clearIntervalMock.mockClear();
    apiMock.mockClear();
  });

  afterAll(() => {
    MockDate.reset();
  });

  test("Constructor should set its certain properties", () => {
    // constructor is called in beforeAll()
    expect({ ...registry[0].construct }).toMatchSnapshot();
  });

  test("Message handler should ignore other recipients", () => {
    const handler = (registry[0].construct as OwnModel & OwnProperties)
      .onDataUpdaterPluginMessage;
    handler("test", {});
    expect(jQueryMock).not.toHaveBeenCalled();
  });

  test.each([
    {
      hasPermission: false,
      permission: permissionsMock.PLUGIN_OCTORELAY_SWITCH,
    },
    {
      hasPermission: true,
      permission: undefined,
    },
  ])(
    "Should not show buttons without permission %#",
    ({ hasPermission, permission }) => {
      hasPermissionMock.mockImplementationOnce(() => hasPermission);
      jest.replaceProperty(
        permissionsMock,
        "PLUGIN_OCTORELAY_SWITCH",
        permission
      );
      const handler = (registry[0].construct as OwnModel & OwnProperties)
        .onDataUpdaterPluginMessage;
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
      expect(hasPermissionMock).toHaveBeenCalledWith({
        test: "I am PLUGIN_OCTORELAY_SWITCH",
      });
      expect(elementMock.toggle).toHaveBeenLastCalledWith(false);
    }
  );
});
