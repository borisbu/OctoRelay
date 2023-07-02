describe("OctoRelayViewModel", () => {
  test("Should push the model into the registry", () => {
    Object.assign(global, {
      OCTOPRINT_VIEWMODELS: [],
      $: jest.fn((cb: () => void) => cb()),
    });

    require("./octorelay");

    expect($).toHaveBeenCalled();
    expect(OCTOPRINT_VIEWMODELS).toHaveLength(1);
  });
});
