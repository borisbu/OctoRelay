import { initOctoRelayModel } from "./model/initOctoRelayModel";
import { describe, vi, test, expect } from "vitest";

describe("Entrypoint", () => {
  const jQueryMock = vi.fn();
  Object.assign(global, {
    $: jQueryMock,
  });
  test("Should set the document onLoad handler", async () => {
    await import("./octorelay");
    expect(jQueryMock).toHaveBeenCalledWith(initOctoRelayModel);
  });
});
