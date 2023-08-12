interface RelayInfo {
  active: boolean;
  confirm_off: boolean;
  icon_html: string;
  label_text: string;
  relay_pin: number;
  inverted_output: boolean;
  relay_state: boolean;
  upcoming: null | {
    deadline: number;
    owner: string;
    state: boolean;
  };
}

type OwnMessage = Record<`r${number}`, RelayInfo>;

type MessageHandler = (plugin: string, data: OwnMessage) => void;

interface OwnProperties {
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

type OwnModel = (
  this: OwnModel & OwnProperties,
  dependencies: object[]
) => void;

$(() => {
  const OctoRelayViewModel: OwnModel = function (
    this,
    [settingsViewModel, loginStateViewModel]
  ) {
    const ownCode = "octorelay";
    const self = this;
    self.settingsViewModel = settingsViewModel;
    self.loginState = loginStateViewModel;

    self.onDataUpdaterPluginMessage = function (plugin, data) {
      if (plugin !== ownCode) {
        return;
      }
      const permission =
        self.settingsViewModel.access?.permissions?.PLUGIN_OCTORELAY_SWITCH;
      const hasPermission =
        permission && self.loginState.hasPermission
          ? self.loginState.hasPermission(permission)
          : false;
      const handleClick = (key: string, value: RelayInfo) => {
        const command = () =>
          OctoPrint.simpleApiCommand(ownCode, "update", { pin: key });
        if (!value.confirm_off) {
          return command();
        }
        const dialog = $("#octorelay-confirmation-dialog");
        dialog
          .find(".modal-title")
          .text("Turning " + value.label_text + " off");
        dialog
          .find("#octorelay-confirmation-text")
          .text(
            "Are you sure you want to turn the " + value.label_text + " off?"
          );
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
      for (const [key, value] of Object.entries(data)) {
        const btn = $("#relais" + key)
          .css({
            display: "flex",
            float: "left",
            width: "40px",
            height: "40px",
            padding: "unset",
            cursor: "pointer",
            "font-size": "1.25rem",
            "text-decoration": "none",
            "align-items": "center",
            "justify-content": "center",
          })
          .toggle(hasPermission && value.active)
          .html(value.icon_html)
          .tooltip("destroy")
          .popover("destroy")
          .attr("title", value.label_text)
          .off("click")
          .on("click", () => handleClick(key, value));
        if (value.upcoming) {
          btn
            .popover({
              html: true,
              placement: "bottom",
              trigger: "manual",
              content: `goes <span class="label">${
                value.upcoming.state ? "ON" : "OFF"
              }</span> at ${new Date(
                value.upcoming.deadline
              ).toLocaleTimeString()} <button class="btn btn-mini" type="button">Avoid</button>`,
            })
            .popover("show");
        } else {
          btn.tooltip({ placement: "bottom" });
        }
      }
    };
  };

  OCTOPRINT_VIEWMODELS.push({
    construct: OctoRelayViewModel,
    dependencies: ["settingsViewModel", "loginStateViewModel"],
  });
});
