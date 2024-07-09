import type { OwnModel } from "../types/OwnModel";
import { makeMessageHandler } from "./messageHandler";

export const OctoRelayViewModel: OwnModel = function (
  this,
  [settingsViewModel, loginStateViewModel],
) {
  this.settingsViewModel = settingsViewModel;
  this.loginState = loginStateViewModel;
  this.onDataUpdaterPluginMessage = makeMessageHandler(this);
};
