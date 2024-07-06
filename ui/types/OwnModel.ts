import type { Relay } from "./Relay";

type Payload = Record<`r${number}`, Relay>;
export type MessageHandler = (plugin: string, data: Payload) => void;

export interface OwnProperties {
  settingsViewModel: {
    access?: {
      permissions?: {
        PLUGIN_OCTORELAY_SWITCH?: object;
      };
    };
  };
  loginState: {
    hasPermission?: (permission: object) => boolean;
  };
  onDataUpdaterPluginMessage: MessageHandler;
}

export type OwnModel = (
  this: OwnModel & OwnProperties,
  dependencies: object[],
) => void;
