import { handlerMock } from "../mocks/messageHandler";
import type { OwnModel, OwnProperties } from "../types/OwnModel";
import { OctoRelayViewModel } from "./OctoRelayModel";

describe("OctoRelayViewModel", () => {
  test("should set certain props of itself", () => {
    const dep1 = jest.fn();
    const dep2 = jest.fn();
    OctoRelayViewModel.call(OctoRelayViewModel as OwnModel & OwnProperties, [
      dep1,
      dep2,
    ]);
    expect(OctoRelayViewModel).toHaveProperty("settingsViewModel", dep1);
    expect(OctoRelayViewModel).toHaveProperty("loginState", dep2);
    expect(OctoRelayViewModel).toHaveProperty(
      "onDataUpdaterPluginMessage",
      handlerMock
    );
  });
});
