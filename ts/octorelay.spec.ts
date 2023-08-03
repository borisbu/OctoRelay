describe("OctoRelayViewModel", () => {
  const registry: ViewModel[] = [];
  const elementMock: Record<
    | "toggle"
    | "html"
    | "attr"
    | "off"
    | "on"
    | "find"
    | "text"
    | "modal"
    | "css",
    jest.Mock
  > = {
    toggle: jest.fn(),
    html: jest.fn(),
    attr: jest.fn(),
    off: jest.fn(() => elementMock),
    on: jest.fn(),
    find: jest.fn(() => elementMock),
    text: jest.fn(),
    modal: jest.fn(),
    css: jest.fn(() => elementMock),
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

  Object.assign(global, {
    OCTOPRINT_VIEWMODELS: registry,
    OctoPrint: { simpleApiCommand: apiMock },
    $: jQueryMock,
  });
  require("./octorelay");

  afterEach(() => {
    jQueryMock.mockClear();
  });

  test("Should push the model into the registry", () => {
    expect(jQueryMock).toHaveBeenCalled();
    expect(registry).toHaveLength(1);
    expect(registry[0]).toMatchSnapshot();
  });

  test("Constructor should set its certain properties", () => {
    const [model] = registry;
    const { construct } = model;
    expect(Object.keys(construct)).toEqual([]);
    construct.call(construct, [
      { access: { permissions: permissionsMock } },
      { hasPermission: hasPermissionMock },
    ]);
    expect({ ...construct }).toMatchSnapshot();
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
      },
      r2: {
        relay_pin: 12,
        inverted_output: true,
        relay_state: true,
        label_text: "Printer",
        active: true,
        icon_html: '<img src="plugin/dashboard/static/img/printer-icon.png">',
        confirm_off: true,
      },
      r3: {
        relay_pin: 18,
        inverted_output: false,
        relay_state: false,
        label_text: "Fan",
        active: true,
        icon_html: '<img src="plugin/dashboard/static/img/fan-icon.png">',
        confirm_off: false,
      },
      r4: {
        relay_pin: 20,
        inverted_output: true,
        relay_state: true,
        label_text: "Chassis Light",
        active: true,
        icon_html: "<div>&#127774;</div>",
        confirm_off: false,
      },
      r5: {
        relay_pin: 24,
        inverted_output: false,
        relay_state: false,
        label_text: "R5",
        active: false,
        icon_html: "ON",
        confirm_off: false,
      },
    });
    expect(hasPermissionMock).toHaveBeenCalledWith({
      test: "I am PLUGIN_OCTORELAY_SWITCH",
    });
    expect(jQueryMock.mock.calls).toMatchSnapshot("$()");
    expect(elementMock.css.mock.calls).toMatchSnapshot(".css()");
    expect(elementMock.toggle.mock.calls).toMatchSnapshot(".toggle()");
    expect(elementMock.html.mock.calls).toMatchSnapshot(".html()");
    expect(elementMock.attr.mock.calls).toMatchSnapshot(".attr()");
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
        },
      });
      expect(hasPermissionMock).toHaveBeenCalledWith({
        test: "I am PLUGIN_OCTORELAY_SWITCH",
      });
      expect(elementMock.toggle).toHaveBeenLastCalledWith(false);
    }
  );
});
