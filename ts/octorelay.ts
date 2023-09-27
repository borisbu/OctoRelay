interface Task {
  deadline: number;
  owner: string;
  target: boolean;
}

interface Relay<U extends null | Task = null | Task> {
  active: boolean;
  confirm_off: boolean;
  icon_html: string;
  label_text: string;
  relay_pin: number;
  inverted_output: boolean;
  relay_state: boolean;
  upcoming: U;
}

type RelayHavingTask = Relay<Task>;

type OwnMessage = Record<`r${number}`, Relay>;

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

interface Hint {
  control: JQuery;
  key: string;
  relay: Relay;
}

interface PopoverItem {
  cancelId: string;
  timeTagId: string;
  deadline: number;
  cancel: () => JQuery.Promise<any>;
}

$(() => {
  const OctoRelayViewModel: OwnModel = function (
    this,
    [settingsViewModel, loginStateViewModel]
  ) {
    const ownCode = "octorelay";
    const self = this;
    self.settingsViewModel = settingsViewModel;
    self.loginState = loginStateViewModel;

    const toggleRelay = (key: string, relay: Relay) => {
      const command = () =>
        OctoPrint.simpleApiCommand(ownCode, "update", { pin: key });
      if (!relay.confirm_off) {
        return command();
      }
      const dialog = $("#octorelay-confirmation-dialog");
      dialog.find(".modal-title").text("Turning " + relay.label_text + " off");
      dialog
        .find("#octorelay-confirmation-text")
        .text(
          "Are you sure you want to turn the " + relay.label_text + " off?"
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

    const hasUpcomingTask = (relay: Relay): relay is RelayHavingTask =>
      relay.upcoming ? relay.upcoming.target !== relay.relay_state : false;

    const clearHints = (btn: JQuery) =>
      btn.tooltip("destroy").popover("destroy");

    const addTooltip = (btn: JQuery, text: string) =>
      btn.tooltip({ placement: "bottom", title: text });

    const showHints = ({
      hints,
      navbar,
    }: {
      hints: Hint[];
      navbar: JQuery;
    }) => {
      const hasMultipleTasks =
        hints.filter(({ relay }) => hasUpcomingTask(relay)).length > 1;
      const popoverCloserId = "pop-closer";
      const closeIconHTML = '<span class="fa fa-close fa-sm"></span>';
      const closeBtnHTML = `<button id="${popoverCloserId}" type="button" class="close">${closeIconHTML}</button>`;
      hints.sort(
        (a, b) =>
          (a.relay.upcoming?.deadline || 0) - (b.relay.upcoming?.deadline || 0)
      );
      let popoverTitle = "";
      let popoverContent: string[] = [];
      let target: JQuery | undefined = undefined;
      let originalSubject = "";
      const popoverItems: PopoverItem[] = [];
      for (const { key, relay, control } of hints) {
        const isRelayHavingTask = hasUpcomingTask(relay);
        if (!isRelayHavingTask || target) {
          addTooltip(control, relay.label_text);
        }
        if (!isRelayHavingTask) {
          continue;
        }
        const { upcoming, label_text: subject } = relay;
        const dateObj = new Date(upcoming.deadline);
        const dateISO = dateObj.toISOString();
        const dateLocalized = dateObj.toLocaleString();
        const timeLeft = formatDeadline(upcoming.deadline);
        const targetState = upcoming.target ? "ON" : "OFF";
        const [cancelId, timeTagId] = ["cancel-btn", "time-tag"].map(
          (prefix) => `${prefix}-${key}`
        );
        popoverItems.push({
          cancelId,
          timeTagId,
          deadline: upcoming.deadline,
          cancel: () => cancelTask(key, upcoming),
        });
        target = target || control;
        originalSubject = originalSubject || subject;
        const upcomingHTML = `${subject} goes <span class="label">${targetState}</span>`;
        const timeHTML = `<time id="${timeTagId}" datetime="${dateISO}" title="${dateLocalized}">${timeLeft}</time>`;
        const cancelHTML = `<button id="${cancelId}" class="btn btn-mini" type="button">Cancel</button>`;
        popoverTitle = hasMultipleTasks
          ? `<span>Several relay switches ahead</span>${closeBtnHTML}`
          : `<span>${upcomingHTML}</span>${closeBtnHTML}`;
        popoverContent.push(
          hasMultipleTasks
            ? `<div><span>${upcomingHTML} ${timeHTML}</span>${cancelHTML}</div>`
            : `<div>${timeHTML}${cancelHTML}</div>`
        );
      }
      if (!target) {
        return;
      }
      target
        .popover({
          html: true,
          animation: false,
          placement: "bottom",
          trigger: "manual",
          title: popoverTitle,
          content: popoverContent.join(""),
        })
        .popover("show");
      const closeBtn = navbar.find(`#${popoverCloserId}`);
      const countdownDisposers = popoverItems.map(
        ({ cancelId, timeTagId, deadline, cancel }) => {
          const cancelBtn = navbar.find(`#${cancelId}`);
          cancelBtn.on("click", cancel);
          const timeTag = navbar.find(`#${timeTagId}`);
          return setCountdown(timeTag, deadline);
        }
      );
      closeBtn.on("click", () => {
        for (const disposer of countdownDisposers) {
          disposer();
        }
        closeBtn.off("click");
        if (target) {
          addTooltip(clearHints(target), originalSubject);
        }
      });
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
  };

  OCTOPRINT_VIEWMODELS.push({
    construct: OctoRelayViewModel,
    dependencies: ["settingsViewModel", "loginStateViewModel"],
  });
});
