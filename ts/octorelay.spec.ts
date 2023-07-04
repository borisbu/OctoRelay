describe("OctoRelayViewModel", () => {
  const registry: ViewModel[] = [];
  const elementMock: Record<
    "toggle" | "html" | "attr" | "off" | "on",
    jest.Mock
  > = {
    toggle: jest.fn(),
    html: jest.fn(),
    attr: jest.fn(),
    off: jest.fn(() => elementMock),
    on: jest.fn(),
  };
  const jQueryMock = jest.fn((subject: string | (() => void)) => {
    if (typeof subject === "function") {
      return subject();
    }
    return elementMock;
  });

  Object.assign(global, {
    OCTOPRINT_VIEWMODELS: registry,
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
        confirmOff: false,
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
    expect(jQueryMock.mock.calls).toMatchSnapshot();
    expect(elementMock.toggle.mock.calls).toMatchSnapshot();
    expect(elementMock.html.mock.calls).toMatchSnapshot();
    expect(elementMock.attr.mock.calls).toMatchSnapshot();
    expect(elementMock.off).toHaveBeenCalledTimes(5);
    expect(elementMock.off).toHaveBeenCalledWith("click");
    expect(elementMock.on).toHaveBeenCalledTimes(5);
    expect(elementMock.on).toHaveBeenCalledWith("click", expect.any(Function));
  });
});
