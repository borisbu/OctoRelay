describe("OctoRelayViewModel", () => {
  const registry: ViewModel[] = [];
  const elementMock: Record<
    "toggle" | "html" | "attr" | "off" | "on" | "find" | "text" | "modal",
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
  };
  const jQueryMock = jest.fn((subject: string | (() => void)) => {
    if (typeof subject === "function") {
      return subject();
    }
    return elementMock;
  });
  const apiMock = jest.fn();

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
    construct.call(construct, [{ settings: true }, { login: true }]);
    expect({ ...construct }).toMatchSnapshot();
  });

  test("Message handler should ignore other recipients", () => {
    const handler = (registry[0].construct as OwnModel & OwnProperties)
      .onDataUpdaterPluginMessage;
    handler("test", {});
    expect(jQueryMock).not.toHaveBeenCalled();
  });

  test("Message handler should process the supplied configuration", () => {
    const handler = (registry[0].construct as OwnModel & OwnProperties)
      .onDataUpdaterPluginMessage;
    handler("octorelay", {
      r1: {
        relay_pin: 16,
        state: 1,
        labelText: "Nozzle Light",
        active: 1,
        iconText: "<div>&#128161;</div>",
        confirmOff: false,
      },
      r2: {
        relay_pin: 12,
        state: 1,
        labelText: "Printer",
        active: 1,
        iconText: '<img src="plugin/dashboard/static/img/printer-icon.png">',
        confirmOff: true,
      },
      r3: {
        relay_pin: 18,
        state: 0,
        labelText: "Fan",
        active: 1,
        iconText: '<img src="plugin/dashboard/static/img/fan-icon.png">',
        confirmOff: false,
      },
      r4: {
        relay_pin: 20,
        state: 1,
        labelText: "Chassis Light",
        active: 1,
        iconText: "<div>&#127774;</div>",
        confirmOff: false,
      },
      r5: {
        relay_pin: 24,
        state: 0,
        labelText: "R5",
        active: 0,
        iconText: "ON",
        confirmOff: false,
      },
    });
    expect(jQueryMock.mock.calls).toMatchSnapshot("$()");
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
});
