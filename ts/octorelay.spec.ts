import MockDate from "mockdate";

describe("OctoRelayViewModel", () => {
  const registry: ViewModel[] = [];
  const elementMock: Record<
    | "toggle"
    | "html"
    | "attr"
    | "removeAttr"
    | "removeData"
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
    attr: jest.fn(() => elementMock),
    removeAttr: jest.fn(() => elementMock),
    removeData: jest.fn(() => elementMock),
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

  Object.assign(global, {
    LOCALE: "en",
    OCTOPRINT_VIEWMODELS: registry,
    OctoPrint: { simpleApiCommand: apiMock },
    $: jQueryMock,
    document: {
      addEventListener: jest.fn(),
      removeEventListener: jest.fn(),
    },
    setInterval: setIntervalMock,
    clearInterval: clearIntervalMock,
  });
  require("./octorelay");

  beforeAll(() => {
    MockDate.set("2023-08-13T22:30:00");
    const [model] = registry;
    const { construct } = model;
    construct.call(construct, [
      { access: { permissions: permissionsMock } },
      { hasPermission: hasPermissionMock },
    ]);
  });

  afterEach(() => {
    jQueryMock.mockClear();
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

  test("Should push the model into the registry", () => {
    expect(jQueryMock).toHaveBeenCalled();
    expect(registry).toHaveLength(1);
    expect(registry[0]).toMatchSnapshot();
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

  test("Message handler should process the supplied configuration", () => {
    hasPermissionMock.mockImplementationOnce(() => true);
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
      r2: {
        relay_pin: 12,
        inverted_output: true,
        relay_state: true,
        label_text: "Printer",
        active: true,
        icon_html: '<img src="plugin/dashboard/static/img/printer-icon.png">',
        confirm_off: true,
        upcoming: null,
      },
      r3: {
        relay_pin: 18,
        inverted_output: false,
        relay_state: false,
        label_text: "Fan",
        active: true,
        icon_html: '<img src="plugin/dashboard/static/img/fan-icon.png">',
        confirm_off: false,
        upcoming: null,
      },
      r4: {
        relay_pin: 20,
        inverted_output: true,
        relay_state: true,
        label_text: "Chassis Light",
        active: true,
        icon_html: "<div>&#127774;</div>",
        confirm_off: false,
        upcoming: null,
      },
      r5: {
        relay_pin: 24,
        inverted_output: false,
        relay_state: false,
        label_text: "R5",
        active: false,
        icon_html: "ON",
        confirm_off: false,
        upcoming: null,
      },
    });
    expect(hasPermissionMock).toHaveBeenCalledWith({
      test: "I am PLUGIN_OCTORELAY_SWITCH",
    });
    expect(jQueryMock.mock.calls).toMatchSnapshot("$()");
    expect(elementMock.toggle.mock.calls).toMatchSnapshot(".toggle()");
    expect(elementMock.html.mock.calls).toMatchSnapshot(".html()");
    expect(elementMock.removeAttr.mock.calls).toMatchSnapshot(".removeAttr()");
    expect(elementMock.removeData.mock.calls).toMatchSnapshot(".removeData()");
    expect(elementMock.attr.mock.calls).toMatchSnapshot(".attr()");
    expect(elementMock.tooltip.mock.calls).toMatchSnapshot(".tooltip()");
    expect(elementMock.popover.mock.calls).toMatchSnapshot(".popover()");
    expect(elementMock.off).toHaveBeenCalledTimes(5);
    expect(elementMock.off).toHaveBeenCalledWith("click");
    expect(elementMock.on).toHaveBeenCalledTimes(5);
    expect(elementMock.on).toHaveBeenCalledWith("click", expect.any(Function));

    // clicking on 1st icon, no confirmation
    elementMock.on.mock.calls[0][1]();
    expect(apiMock).toHaveBeenCalledTimes(1);
    expect(apiMock).toHaveBeenCalledWith("octorelay", "update", { pin: "r1" });
    expect(elementMock.on).toHaveBeenCalledTimes(5); // remains

    // clicking on 2nd icon, with confirmation
    elementMock.on.mock.calls[1][1]();
    expect(apiMock).toHaveBeenCalledTimes(1);
    expect(elementMock.find.mock.calls).toMatchSnapshot(".find()");
    expect(elementMock.text.mock.calls).toMatchSnapshot(".text()");
    expect(elementMock.modal).toHaveBeenCalledTimes(1);
    expect(elementMock.modal).toHaveBeenCalledWith("show");
    expect(elementMock.on).toHaveBeenCalledTimes(7);

    // clicking cancel button of the modal
    elementMock.on.mock.calls[5][1]();
    expect(elementMock.modal).toHaveBeenCalledTimes(2);
    expect(elementMock.modal).toHaveBeenLastCalledWith("hide");
    expect(apiMock).toHaveBeenCalledTimes(1); // remains

    // clicking confirm button of the modal
    elementMock.on.mock.calls[6][1]();
    expect(jQueryMock).toHaveBeenCalledWith("#octorelay-confirmation-dialog");
    expect(elementMock.modal).toHaveBeenCalledTimes(3);
    expect(elementMock.modal).toHaveBeenLastCalledWith("hide");
    expect(apiMock).toHaveBeenCalledTimes(2);
    expect(apiMock).toHaveBeenLastCalledWith("octorelay", "update", {
      pin: "r2",
    });
  });

  test.each([15, 150, 5000])(
    "Should display upcoming state popover (%s sec delay)",
    (delay) => {
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
          upcoming: {
            target: false,
            owner: "PRINTING_STOPPED",
            deadline: Date.now() + delay * 1000,
          },
        },
      });
      expect(elementMock.popover.mock.calls).toMatchSnapshot(".popover()");
    }
  );

  test.each([true, false])("Should set countdown %#", (isVisible) => {
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
        upcoming: {
          target: false,
          owner: "PRINTING_STOPPED",
          deadline: Date.now() + 20 * 1000,
        },
      },
    });
    expect(setIntervalMock).toHaveBeenCalledWith(expect.any(Function), 1000);
    const intervalFn = setIntervalMock.mock.calls[0][0];
    elementMock.is.mockImplementationOnce(() => isVisible);
    intervalFn();
    if (isVisible) {
      expect(elementMock.text).toHaveBeenCalledWith("in 20 seconds");
    } else {
      expect(elementMock.text).not.toHaveBeenCalled();
      expect(clearIntervalMock).toHaveBeenCalledWith("mockedInterval");
    }
  });

  test("Clicking on Cancel button should send the command", () => {
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
        upcoming: {
          target: false,
          owner: "PRINTING_STOPPED",
          deadline: Date.now() + 150 * 1000,
        },
      },
    });
    expect(elementMock.on).toHaveBeenCalledTimes(3); // controlBtn, closeBtn, cancelBtn
    const cancelHandler = elementMock.on.mock.calls[2][1];
    cancelHandler();
    expect(apiMock).toHaveBeenCalledWith("octorelay", "cancelTask", {
      owner: "PRINTING_STOPPED",
      subject: "r1",
      target: false,
    });
  });

  test("Clicking on Cancel button should send the command", () => {
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
        upcoming: {
          target: false,
          owner: "PRINTING_STOPPED",
          deadline: Date.now() + 150 * 1000,
        },
      },
    });
    expect(elementMock.on).toHaveBeenCalledTimes(3); // controlBtn, closeBtn, cancelBtn
    const closeHandler = elementMock.on.mock.calls[1][1];
    closeHandler();
    expect(elementMock.popover).toHaveBeenCalledWith("hide");
    expect(clearIntervalMock).toHaveBeenCalledWith("mockedInterval");
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
