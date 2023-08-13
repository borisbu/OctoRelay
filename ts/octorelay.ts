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
    target: boolean;
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

    const toggleRelay = (key: string, value: RelayInfo) => {
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

    const cancelPostponedTask = (key: string, value: RelayInfo) =>
      OctoPrint.simpleApiCommand(ownCode, "cancelTask", {
        subject: key,
        owner: value.upcoming?.owner,
        target: value.upcoming?.target,
      });

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
      const formattedTimeLeft = new Intl.NumberFormat(LOCALE, {
        style: "unit",
        unitDisplay: "long",
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
        unit,
      }).format(timeLeft);
      return `in ${formattedTimeLeft}`;
    };

    const onClickOutside = (selector: JQuery, handler: () => void) => {
      const listener = (event: MouseEvent) => {
        const target = $(event.target!); // !
        if (!target.closest(selector).length) {
          if (selector.is(":visible")) {
            handler();
          }
          document.removeEventListener("click", listener); // disposer
        }
      };
      document.addEventListener("click", listener);
    };

    const getCountdownDelay = (deadline: number): number =>
      deadline - Date.now() > 120000 ? 60000 : 1000;

    const setCountdown = (selector: JQuery, deadline: number) => {
      const delay = getCountdownDelay(deadline);
      const interval = setInterval(() => {
        const disposer = () => clearInterval(interval);
        const isVisible = selector.is(":visible");
        if (!isVisible) {
          disposer();
          return;
        }
        selector.text(formatDeadline(deadline));
        const nextDelay = getCountdownDelay(deadline);
        if (nextDelay !== delay) {
          disposer();
          setCountdown(selector, deadline); // reset with new interval
        }
      }, delay);
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
        const relayBtn = $(`#navbar_plugin_octorelay #relais${key}`)
          .toggle(hasPermission && value.active)
          .html(value.icon_html)
          .tooltip("destroy")
          .popover("destroy")
          .removeData("original-title")
          .removeAttr("data-original-title")
          .removeAttr("title")
          .off("click")
          .on("click", () => toggleRelay(key, value));
        if (value.upcoming && value.upcoming.target !== value.relay_state) {
          const dateObj = new Date(value.upcoming.deadline);
          relayBtn
            .popover({
              html: true,
              placement: "bottom",
              trigger: "manual",
              title: `<span>${value.label_text} goes <span class="label">${
                value.upcoming.target ? "ON" : "OFF"
              }</span></span><button id="pop-closer-${key}" type="button" class="close"><span class="fa fa-close fa-sm"></span></button>`,
              content: `<time id="time-tag-${key}" datetime="${dateObj.toISOString()}" title="${dateObj.toLocaleString()}">${formatDeadline(
                value.upcoming.deadline
              )}</time><button id="cancel-btn-${key}" class="btn btn-mini" type="button">Cancel</button>`,
            })
            .popover("show");
          const closeBtn = $(`#navbar_plugin_octorelay #pop-closer-${key}`);
          const cancelBtn = $(`#navbar_plugin_octorelay #cancel-btn-${key}`);
          const timeTag = $(`#navbar_plugin_octorelay #time-tag-${key}`);
          setCountdown(timeTag, value.upcoming.deadline);
          const closePopover = () => {
            closeBtn.off("click");
            relayBtn.popover("hide");
          };
          closeBtn.on("click", closePopover);
          onClickOutside(closeBtn.closest(".popover"), closePopover);
          cancelBtn.on("click", () => cancelPostponedTask(key, value));
        } else {
          relayBtn
            .attr("title", value.label_text)
            .tooltip({ placement: "bottom" });
        }
      }
    };
  };

  OCTOPRINT_VIEWMODELS.push({
    construct: OctoRelayViewModel,
    dependencies: ["settingsViewModel", "loginStateViewModel"],
  });
});
