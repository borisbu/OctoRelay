"use strict";
$(function () {
    var OctoRelayViewModel = function (_a) {
        var settingsViewModel = _a[0], loginStateViewModel = _a[1];
        var ownCode = "octorelay";
        var self = this;
        self.settingsViewModel = settingsViewModel;
        self.loginState = loginStateViewModel;
        self.onDataUpdaterPluginMessage = function (plugin, data) {
            if (plugin !== ownCode) {
                return;
            }
            var handleClick = function (key, value) {
                var command = function () {
                    return OctoPrint.simpleApiCommand(ownCode, "update", { pin: key });
                };
                if (!value.confirmOff) {
                    return command();
                }
                var dialog = $("#octorelay-confirmation-dialog");
                dialog.find(".modal-title").text("Turning " + value.labelText + " off");
                dialog
                    .find("#octorelay-confirmation-text")
                    .text("Are you sure you want to turn the " + value.labelText + " off?");
                dialog
                    .find(".btn-cancel")
                    .off("click")
                    .on("click", function () { return dialog.modal("hide"); });
                dialog
                    .find(".btn-confirm")
                    .off("click")
                    .on("click", function () {
                    command();
                    dialog.modal("hide");
                });
                dialog.modal("show");
            };
            var _loop_1 = function (key, value) {
                var btn = $("#relais" + key);
                if (value.active !== undefined) {
                    btn.toggle(value.active === 1);
                }
                var icon = $("#ralayIcon" + key);
                if (value.iconText !== undefined) {
                    icon.html(value.iconText);
                }
                if (value.labelText !== undefined) {
                    icon.attr("title", value.labelText);
                }
                icon.off("click").on("click", function () { return handleClick(key, value); });
            };
            for (var _i = 0, _a = Object.entries(data); _i < _a.length; _i++) {
                var _b = _a[_i], key = _b[0], value = _b[1];
                _loop_1(key, value);
            }
        };
    };
    OCTOPRINT_VIEWMODELS.push({
        construct: OctoRelayViewModel,
        dependencies: ["settingsViewModel", "loginStateViewModel"],
    });
});
