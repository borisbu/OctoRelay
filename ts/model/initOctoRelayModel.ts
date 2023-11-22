import { OctoRelayViewModel } from "./OctoRelayModel";

export const initOctoRelayModel = () => {
  OCTOPRINT_VIEWMODELS.push({
    construct: OctoRelayViewModel,
    dependencies: ["settingsViewModel", "loginStateViewModel"],
  });
};
