"use strict";
$(() => {
    const OctoRelayViewModel = function ([settingsViewModel, loginStateViewModel]) {
        const ownCode = "octorelay";
        const self = this;
        self.settingsViewModel = settingsViewModel;
        self.loginState = loginStateViewModel;
        const toggleRelay = (key, value) => {
            const command = () => OctoPrint.simpleApiCommand(ownCode, "update", { pin: key });
            if (!value.confirm_off) {
                return command();
            }
            const dialog = $("#octorelay-confirmation-dialog");
            dialog.find(".modal-title").text("Turning " + value.label_text + " off");
            dialog
                .find("#octorelay-confirmation-text")
                .text("Are you sure you want to turn the " + value.label_text + " off?");
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
        const cancelPostponedTask = (key, value) => {
            var _a, _b;
            return OctoPrint.simpleApiCommand(ownCode, "cancelTask", {
                subject: key,
                owner: (_a = value.upcoming) === null || _a === void 0 ? void 0 : _a.owner,
                target: (_b = value.upcoming) === null || _b === void 0 ? void 0 : _b.target,
            });
        };
        const formatDeadline = (time) => {
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
        const onClickOutside = (selector, handler) => {
            const listener = (event) => {
                const target = $(event.target);
                if (!target.closest(selector).length) {
                    if (selector.is(":visible")) {
                        handler();
                    }
                    document.removeEventListener("click", listener);
                }
            };
            document.addEventListener("click", listener);
        };
        const getCountdownDelay = (deadline) => deadline - Date.now() > 120000 ? 60000 : 1000;
        const setCountdown = (selector, deadline) => {
            const delay = getCountdownDelay(deadline);
            let disposer;
            const interval = setInterval(() => {
                const isVisible = selector.is(":visible");
                if (!isVisible) {
                    return disposer();
                }
                selector.text(formatDeadline(deadline));
                const nextDelay = getCountdownDelay(deadline);
                if (nextDelay !== delay) {
                    disposer();
                    disposer = setCountdown(selector, deadline);
                }
            }, delay);
            disposer = () => clearInterval(interval);
            return disposer;
        };
        self.onDataUpdaterPluginMessage = function (plugin, data) {
            var _a, _b;
            if (plugin !== ownCode) {
                return;
            }
            const permission = (_b = (_a = self.settingsViewModel.access) === null || _a === void 0 ? void 0 : _a.permissions) === null || _b === void 0 ? void 0 : _b.PLUGIN_OCTORELAY_SWITCH;
            const hasPermission = permission && self.loginState.hasPermission
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
                        title: `<span>${value.label_text} goes <span class="label">${value.upcoming.target ? "ON" : "OFF"}</span></span><button id="pop-closer-${key}" type="button" class="close"><span class="fa fa-close fa-sm"></span></button>`,
                        content: `<time id="time-tag-${key}" datetime="${dateObj.toISOString()}" title="${dateObj.toLocaleString()}">${formatDeadline(value.upcoming.deadline)}</time><button id="cancel-btn-${key}" class="btn btn-mini" type="button">Cancel</button>`,
                    })
                        .popover("show");
                    const closeBtn = $(`#navbar_plugin_octorelay #pop-closer-${key}`);
                    const cancelBtn = $(`#navbar_plugin_octorelay #cancel-btn-${key}`);
                    const timeTag = $(`#navbar_plugin_octorelay #time-tag-${key}`);
                    const countdownDisposer = setCountdown(timeTag, value.upcoming.deadline);
                    const closePopover = () => {
                        countdownDisposer();
                        closeBtn.off("click");
                        relayBtn.popover("hide");
                    };
                    closeBtn.on("click", closePopover);
                    onClickOutside(closeBtn.closest(".popover"), closePopover);
                    cancelBtn.on("click", () => cancelPostponedTask(key, value));
                }
                else {
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
