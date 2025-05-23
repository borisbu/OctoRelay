import { lodashMock } from "./mocks/lodash";

describe("Entrypoint", () => {
  const jQueryMock = vi.fn();
  Object.assign(global, {
    $: jQueryMock,
    _: lodashMock,
  });
  test("Should set the document onLoad handler", async () => {
    const { initOctoRelayModel } = await import("./model/initOctoRelayModel");
    await import("./octorelay");
    expect(jQueryMock).toHaveBeenCalledWith(initOctoRelayModel);
  });
});
