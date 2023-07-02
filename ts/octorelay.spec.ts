describe("OctoRelayViewModel", () => {
  const registry: ViewModel[] = [];
  const jQueryMock = jest.fn((cb: () => void) => cb());

  Object.assign(global, {
    OCTOPRINT_VIEWMODELS: registry,
    $: jQueryMock,
  });
  require("./octorelay");

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
});
