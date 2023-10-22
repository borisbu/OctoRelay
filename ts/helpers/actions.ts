import type { Relay, Task } from "../types/Relay";
import { ownCode } from "./const";

export const toggleRelay = (key: string, relay: Relay) => {
  const command = () =>
    OctoPrint.simpleApiCommand(ownCode, "update", { v: 2, subject: key });
  if (!relay.confirm_off) {
    return command();
  }
  const dialog = $("#octorelay-confirmation-dialog");
  dialog.find(".modal-title").text("Turning " + relay.label_text + " off");
  dialog
    .find("#octorelay-confirmation-text")
    .text("Are you sure you want to turn the " + relay.label_text + " off?");
  dialog
    .find(".btn-cancel")
    .off("click")
    .on("click", () => dialog.modal("hide"));
  dialog
    .find(".btn-confirm")
    .off("click")
    .on("click", () => {
      command();
      dialog.modal("hide");
    });
  dialog.modal("show");
};

export const cancelTask = (key: string, { owner, target }: Task) =>
  OctoPrint.simpleApiCommand(ownCode, "cancelTask", {
    v: 2,
    subject: key,
    owner,
    target,
  });
