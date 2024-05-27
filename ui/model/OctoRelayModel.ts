import type { OwnModel } from "../types/OwnModel";
import { makeMessageHandler } from "./messageHandler";

export const OctoRelayViewModel: OwnModel = function (
  this,
  [settingsViewModel, loginStateViewModel],
) {
  // eslint-disable-next-line @typescript-eslint/no-this-alias
  const self = this;
  self.settingsViewModel = settingsViewModel;
  self.loginState = loginStateViewModel;
  self.onDataUpdaterPluginMessage = makeMessageHandler(self);
};
