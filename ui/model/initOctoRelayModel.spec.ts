import { modelMock } from "../mocks/OctoRelayModel";
import { initOctoRelayModel } from "./initOctoRelayModel";
import { describe, test, expect } from "vitest";

describe("initOctorelayModel()", () => {
  const registryMock: ViewModel[] = [];

  Object.assign(global, {
    OCTOPRINT_VIEWMODELS: registryMock,
  });

  test("should add the plugin model into the registry", () => {
    initOctoRelayModel();
    expect(registryMock).toHaveLength(1);
    expect(registryMock[0].construct).toEqual(modelMock);
  });
});
