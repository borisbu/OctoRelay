import { initOctoRelayModel } from "./model/initOctoRelayModel";

describe("Entrypoint", () => {
  const jQueryMock = jest.fn();
  Object.assign(global, {
    $: jQueryMock,
  });
  test("Should set the document onLoad handler", async () => {
    await import("./octorelay");
    expect(jQueryMock).toHaveBeenCalledWith(initOctoRelayModel);
  });
});
