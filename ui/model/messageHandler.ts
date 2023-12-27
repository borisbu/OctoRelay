import { ownCode } from "../helpers/const";
import { clearHints, showHints } from "../helpers/hints";
import { toggleRelay } from "../helpers/actions";
import type { Hint } from "../types/Hints";
import type {
  MessageHandler,
  OwnModel,
  OwnProperties,
} from "../types/OwnModel";

export const makeMessageHandler =
  (model: OwnModel & OwnProperties): MessageHandler =>
  (plugin, data) => {
    if (plugin !== ownCode) {
      return;
    }
    const permission =
      model.settingsViewModel.access?.permissions?.PLUGIN_OCTORELAY_SWITCH;
    const hasPermission =
      permission && model.loginState.hasPermission
        ? model.loginState.hasPermission(permission)
        : false;
    const navbar = $(`#navbar_plugin_${ownCode}`);
    const hints: Hint[] = [];
    for (const [key, relay] of Object.entries(data)) {
      const control = navbar
        .find(`#relais${key}`)
        .toggle(hasPermission && relay.active)
        .html(relay.icon_html)
        .off("click")
        .on("click", () => toggleRelay(key, relay));
      clearHints(control);
      hints.push({ control, key, relay });
    }
    showHints({ hints, navbar });
  };
