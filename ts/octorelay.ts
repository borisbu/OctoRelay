interface Task {
  deadline: number;
  owner: string;
  target: boolean;
}

interface RelayInfo {
  active: boolean;
  confirm_off: boolean;
  icon_html: string;
  label_text: string;
  relay_pin: number;
  inverted_output: boolean;
  relay_state: boolean;
  upcoming: null | Task;
}

type RelayHavingTask = RelayInfo & {
  upcoming: NonNullable<RelayInfo["upcoming"]>;
};

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

    const cancelTask = (key: string, { owner, target }: Task) =>
      OctoPrint.simpleApiCommand(ownCode, "cancelTask", {
        subject: key,
        owner,
        target,
      });

    const formatDeadline = (time: number): string => {
      let unit: "second" | "minute" | "hour" = "second";
      let timeLeft = (time - Date.now()) / 1000;
      if (timeLeft >= 60) {
        timeLeft /= 60;
        unit = "minute";
      }
      if (timeLeft >= 60) {
        timeLeft /= 60;
        unit = "hour";
      }
      const isLastMinute = unit === "minute" && timeLeft < 2;
      const formattedTimeLeft = new Intl.NumberFormat(LOCALE, {
        style: "unit",
        unitDisplay: "long",
        minimumFractionDigits: isLastMinute ? 1 : 0,
        maximumFractionDigits: isLastMinute ? 1 : 0,
        unit,
      }).format(Math.max(0, timeLeft));
      return `in ${formattedTimeLeft}`;
    };

    const getCountdownDelay = (deadline: number): number =>
      deadline - Date.now() > 120000 ? 60000 : 1000;

    const setCountdown = (selector: JQuery, deadline: number): (() => void) => {
      const delay = getCountdownDelay(deadline);
      let disposer: () => void;
      const interval = setInterval(() => {
        const isVisible = selector.is(":visible");
        if (!isVisible) {
          return disposer();
        }
        selector.text(formatDeadline(deadline));
        const nextDelay = getCountdownDelay(deadline);
        if (nextDelay !== delay) {
          disposer();
          disposer = setCountdown(selector, deadline); // reset with new interval
        }
      }, delay);
      disposer = () => clearInterval(interval);
      return disposer;
    };

    const hasUpcomingTask = (value: RelayInfo): value is RelayHavingTask =>
      value.upcoming ? value.upcoming.target !== value.relay_state : false;

    const clearHints = (btn: JQuery) =>
      btn.tooltip("destroy").popover("destroy");

    const addTooltip = (btn: JQuery, text: string) =>
      btn.tooltip({ placement: "bottom", title: text });

    const addPopover = ({
      relayBtn,
      key,
      value: { label_text: subject, upcoming },
      navbar,
    }: {
      relayBtn: JQuery;
      key: string;
      value: RelayHavingTask;
      navbar: JQuery;
    }) => {
      const dateObj = new Date(upcoming.deadline);
      const dateISO = dateObj.toISOString();
      const dateLocalized = dateObj.toLocaleString();
      const timeLeft = formatDeadline(upcoming.deadline);
      const targetState = upcoming.target ? "ON" : "OFF";
      const [closerId, cancelId, timeTagId] = [
        "pop-closer",
        "cancel-btn",
        "time-tag",
      ].map((prefix) => `${prefix}-${key}`);
      const upcomingHTML = `<span>${subject} goes <span class="label">${targetState}</span></span>`;
      const closeIconHTML = '<span class="fa fa-close fa-sm"></span>';
      const closeBtnHTML = `<button id="${closerId}" type="button" class="close">${closeIconHTML}</button>`;
      const timeHTML = `<time id="${timeTagId}" datetime="${dateISO}" title="${dateLocalized}">${timeLeft}</time>`;
      const cancelHTML = `<button id="${cancelId}" class="btn btn-mini" type="button">Cancel</button>`;
      relayBtn
        .popover({
          html: true,
          placement: "bottom",
          trigger: "manual",
          title: `${upcomingHTML}${closeBtnHTML}`,
          content: `${timeHTML}${cancelHTML}`,
        })
        .popover("show");
      const closeBtn = navbar.find(`#${closerId}`);
      const cancelBtn = navbar.find(`#${cancelId}`);
      const timeTag = navbar.find(`#${timeTagId}`);
      const countdownDisposer = setCountdown(timeTag, upcoming.deadline);
      closeBtn.on("click", () => {
        countdownDisposer();
        closeBtn.off("click");
        addTooltip(clearHints(relayBtn), subject);
      });
      cancelBtn.on("click", () => cancelTask(key, upcoming));
      return relayBtn;
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
      const navbar = $(`#navbar_plugin_${ownCode}`);
      const upcomingStack: Array<Parameters<typeof addPopover>[0]> = [];
      for (const [key, value] of Object.entries(data)) {
        const relayBtn = navbar
          .find(`#relais${key}`)
          .toggle(hasPermission && value.active)
          .html(value.icon_html)
          .off("click")
          .on("click", () => toggleRelay(key, value));
        clearHints(relayBtn);
        if (hasUpcomingTask(value)) {
          upcomingStack.push({ relayBtn, key, value, navbar });
        } else {
          addTooltip(relayBtn, value.label_text);
        }
        upcomingStack.sort(
          (a, b) => a.value.upcoming.deadline - b.value.upcoming.deadline
        );
        upcomingStack.forEach(addPopover); // @todo continue here
      }
    };
  };

  OCTOPRINT_VIEWMODELS.push({
    construct: OctoRelayViewModel,
    dependencies: ["settingsViewModel", "loginStateViewModel"],
  });
});
