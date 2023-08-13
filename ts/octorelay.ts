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

    const handleClick = (key: string, value: RelayInfo) => {
      const command = () =>
        OctoPrint.simpleApiCommand(ownCode, "update", { pin: key });
      if (!value.confirm_off) {
        return command();
      }
      const dialog = $("#octorelay-confirmation-dialog");
      dialog.find(".modal-title").text("Turning " + value.label_text + " off");
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

    const formatDeadline = (time: number): string => {
      let unit = "second";
      let timeLeft = (time - Date.now()) / 1000;
      if (timeLeft >= 60) {
        timeLeft /= 60;
        unit = "minute";
      }
      if (timeLeft >= 60) {
        timeLeft /= 60;
        unit = "hour";
      }
      return new Intl.NumberFormat(LOCALE || "en", {
        style: "unit",
        unitDisplay: "long",
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
        unit,
      }).format(timeLeft);
    };

    const onClickOutside = (selector: JQuery, handler: () => void) => {
      const listener = (event: MouseEvent) => {
        if (!event.target) {
          return;
        }
        const target = $(event.target);
        if (!target.closest(selector).length) {
          if ($(selector).is(":visible")) {
            handler();
          }
          document.removeEventListener("click", listener); // disposer
        }
      };
      document.addEventListener("click", listener);
    };

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
      for (const [key, value] of Object.entries(data)) {
        const btn = $(`#navbar_plugin_octorelay #relais${key}`)
          .toggle(hasPermission && value.active)
          .html(value.icon_html)
          .removeAttr("title")
          .tooltip("destroy")
          .popover("destroy")
          .off("click")
          .on("click", () => handleClick(key, value));
        if (value.upcoming) {
          const dateObj = new Date(value.upcoming.deadline);
          btn
            .popover({
              html: true,
              placement: "bottom",
              trigger: "manual",
              title: `<span>${value.label_text} goes <span class="label">${
                value.upcoming.state ? "ON" : "OFF"
              }</span></span><button id="pop-closer-${key}" type="button" class="close"><span class="fa fa-close fa-sm"></span></button>`,
              content: `<time datetime="${dateObj.toISOString()}" title="${dateObj.toLocaleString()}">in ${formatDeadline(
                value.upcoming.deadline
              )}</time><button class="btn btn-mini" type="button">Cancel</button>`,
            })
            .popover("show");
          const closer = $(`#navbar_plugin_octorelay #pop-closer-${key}`);
          const handleCloseClick = () => {
            closer.off("click");
            btn.popover("hide");
          };
          closer.on("click", handleCloseClick);
          onClickOutside(closer.closest(".popover"), handleCloseClick);
        } else {
          btn.attr("title", value.label_text).tooltip({ placement: "bottom" });
        }
      }
    };
  };

  OCTOPRINT_VIEWMODELS.push({
    construct: OctoRelayViewModel,
    dependencies: ["settingsViewModel", "loginStateViewModel"],
  });
});
